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
      // const actions = parseAction(body);
      // action could be of the type { type: "up", "down", "review", "summary", "help" }, these action will only work for a PR.
      const turtleActions = ["summary"];
      for (const action of turtleActions) {
        switch (action) {
          case "summary":
            await handlePullRequestSummary(body, installationId);
            break;
          case "review":
            await handlePullRequestReview(body, installationId);
            break;
        }
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
