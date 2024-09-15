import {
  handlePullRequestReview,
  handlePullRequestSummary,
  handleInstallation,
  handleIssue,
} from "../services/octokit.service.js";

async function handleWebhookEvent(body, event, installationId) {
  console.log("Handling webhook event", event, body, installationId);
  // look for evoke commands here, and update the db.
  // was it a up or down command or does it contain an action command.
  // if it was an action command, then we need to check if the user has the permission to perform the action.
  switch (event) {
    case "pull_request":
      // Grab the action from the payload
      const action = body.action;

      switch (action) {
        case "opened":
          // Pull out the turtle tasks from the payload, still need to implement this.
          const turtleTasks = ["summary"]; // could be an array of tasks like ["summary", "review"]
          for (const task of turtleTasks) {
            switch (task) {
              case "summary":
                await handlePullRequestSummary(body, installationId);
                //TODO: Add Indetifier to the comment
                break;
              case "review":
                await handlePullRequestReview(body, installationId);
                break;
            }
            break;
          }
        case "synchronize" || "edited":
        //TODO:Get the identifier from the comment and update the comment, the identifier is a hidden comment

      }
      break;

    case "installation":
      await handleInstallation(body);
      break;

    case "issues":
      await handleIssue(body, installationId);
      break;
  }
}

export { handleWebhookEvent };
