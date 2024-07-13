/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Probot} app
 */
import * as express from "express";

export default (app, { getRouter }) => {
  // Your code here
  app.log.info("Yay, the app was loaded!");

  app.on("issues.opened", async (context) => {
    console.log(context);
    context.log.info("Issue opened event fired", context.name);
    const issueComment = context.issue({
      body: "Thanks for opening this issue!",
    });
    return context.octokit.issues.createComment(issueComment);
  });

  app.on("pull_request.opened", async (context) => {
    const prNumber = context.payload.pull_request.number;
    const owner = context.payload.repository.owner.login;
    const repo = context.payload.repository.name;

    const diffUrl = context.payload.pull_request.diff_url;

    const prComment = context.issue({
      body: `Thanks for opening this pull request! You can view the diffs [here](${diffUrl}).`,
    });
    return context.octokit.issues.createComment(prComment);
  });

  app.on("pull_request.edited", async (context) => {
    context.log.info("Edit event fired", context.name);
    context.log.info(context.payload.pull_request);
    const prNumber = context.payload.pull_request.number;
    const owner = context.payload.repository.owner.login;
    const repo = context.payload.repository.name;

    const diffUrl = context.payload.pull_request.diff_url;

    const prComment = context.issue({
      body: `This pull request! has been edited.`,
    });
    return context.octokit.issues.createComment(prComment);
  });

  const router = getRouter("/api");
  router.use(express.json());
  // Add a new route
  router.get("/hello-world", (req, res) => {
    res.send("Hello World");
  });

  router.post('/process-event', async (req, res) => {
    try{
      // const octokit = await app.auth({type: "installation", installationId: 52567932});
      // console.log(octokit);
      const octokit = await app.auth(52567932);
      const { type, payload } = req.body;
      // console.log(app);
      if (type === 'issue_opened') {
        const issueComment = {
          owner: payload.repository.owner.login,
          repo: payload.repository.name,
          issue_number: payload.issue_number.number,
          body: 'Your issue has been processed!',
        };
        await octokit.issues.createComment(issueComment);
      } else if (type === 'pull_request_opened' || type === 'pull_request_edited') {
        const prComment = {
          owner: payload.repository.owner.login,
          repo: payload.repository.name,
          issue_number: payload.pull_request.number,
          body: 'Your pull request has been processed!',
        };
        await octokit.issues.createComment(prComment);
      }
      res.status(200).send('Event processed');
    } catch (error) {
      console.log(error);
      res.status(500).send('Error processing event');
    }
  });

  // app.onAny(async (context) => {
  //   context.log.info("New event fired", context.name);
  // });

  // For more information on building apps:
  // https://probot.github.io/docs/

  // To get your app running against GitHub, see:
  // https://probot.github.io/docs/development/
};
