import { createNodeMiddleware, Probot } from 'probot';
import AWS from 'aws-sdk';
import express from 'express';
import fs from 'fs';
import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

// Initialize express app
const expressApp = express();
expressApp.use(express.json()); // Middleware to parse JSON bodies

// Configure AWS SDK
const sqs = new AWS.SQS({ region: 'your-region' });
const queueUrl = 'your-sqs-queue-url';

const sendToSQS = async (message) => {
  const params = {
    QueueUrl: queueUrl,
    MessageBody: JSON.stringify(message),
  };
  try {
    await sqs.sendMessage(params).promise();
  } catch (error) {
    console.error('Error sending message to SQS:', error);
  }
};

// Read the private key from file
let privateKey;
try {
  privateKey = fs.readFileSync(process.env.PRIVATE_KEY_PATH, 'utf8');
} catch (error) {
  console.error('Error reading private key:', error);
  process.exit(1); // Exit if the private key cannot be read
}

// Validate environment variables
const appId = process.env.APP_ID;
const webhookSecret = process.env.WEBHOOK_SECRET;

if (!appId || !webhookSecret) {
  console.error('APP_ID and WEBHOOK_SECRET environment variables must be set');
  process.exit(1);
}

// Probot app function
const probotApp = (app) => {
  app.log.info("Yay, the app was loaded!");

  app.on("issues.opened", async (context) => {
    try {
      console.log("Issue opened event fired", context);
      const issueComment = context.issue({
        body: "Thanks for opening this issue!",
      });
      await context.octokit.issues.createComment(issueComment);
    } catch (error) {
      context.log.error('Error handling issues.opened event:', error);
    }
  });

  app.on("pull_request.opened", async (context) => {
    try {
      const prNumber = context.payload.pull_request.number;
      const diffUrl = context.payload.pull_request.diff_url;

      const prComment = context.issue({
        body: `Thanks for opening this pull request! You can view the diffs [here](${diffUrl}).`,
      });
      await context.octokit.issues.createComment(prComment);
    } catch (error) {
      context.log.error('Error handling pull_request.opened event:', error);
    }
  });

  app.on("pull_request.edited", async (context) => {
    try {
      context.log.info("Edit event fired", context);
      const prComment = context.issue({
        body: `This pull request has been edited.`,
      });
      await context.octokit.issues.createComment(prComment);
    } catch (error) {
      context.log.error('Error handling pull_request.edited event:', error);
    }
  });

  app.on("pull_request.synchronize", async (context) => {
    try {
      context.log.info("Synchronize event fired", context.name);
      const prComment = context.issue({
        body: `This pull request has been synchronized.`,
      });
      await context.octokit.issues.createComment(prComment);
    } catch (error) {
      context.log.error('Error handling pull_request.synchronize event:', error);
    }
  });
};

// Initialize Probot with the express app
const probot = new Probot({
  appId: appId,
  privateKey: privateKey,
  secret: webhookSecret,
});

try {
  probot.load(probotApp);
  console.log('Probot app loaded successfully');
} catch (error) {
  console.error('Error loading Probot app:', error);
  process.exit(1); // Exit if Probot app fails to load
}

// Use Probot's webhook middleware with the express app
expressApp.use('/api/github/webhooks', createNodeMiddleware(probotApp, { probot }));

// Custom endpoint to receive callbacks from cloud processing
expressApp.post('/process-event', async (req, res) => {
  try {
    const { type, payload } = req.body;

    if (type === 'issue_opened') {
      const issueComment = {
        owner: payload.repository.owner.login,
        repo: payload.repository.name,
        issue_number: payload.issue.number,
        body: 'Your issue has been processed!',
      };
      await probot.octokit.issues.createComment(issueComment);
    } else if (type === 'pull_request_opened' || type === 'pull_request_edited') {
      const prComment = {
        owner: payload.repository.owner.login,
        repo: payload.repository.name,
        issue_number: payload.pull_request.number,
        body: 'Your pull request has been processed!',
      };
      await probot.octokit.issues.createComment(prComment);
    }

    res.status(200).send('Event processed');
  } catch (error) {
    console.error('Error processing event:', error);
    res.status(500).send('Internal Server Error');
  }
});

// Start the express server
const port = process.env.PORT || 3000;
expressApp.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
