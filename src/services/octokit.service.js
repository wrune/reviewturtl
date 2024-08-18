import { Octokit } from "@octokit/rest";
import { createAppAuth } from "@octokit/auth-app";
import config from "../constants/config.js";
import { turtle } from "./turtle.service.js";

const createOctokit = (installationId) =>
  new Octokit({
    authStrategy: createAppAuth,
    auth: {
      appId: config.GITHUB_APP_ID,
      privateKey: config.GITHUB_PRIVATE_KEY,
      installationId: installationId,
    },
  });

const handlePullRequestReview = async (payload, installationId) => {
  const response = await turtle.review(payload);
  const octokit = createOctokit(installationId);
  // Implement your PR review handling logic here.
  octokit.pulls.createReview({
    owner: payload.repository.owner.login,
    repo: payload.repository.name,
    pull_number: payload.pull_request.number,
    body: response.summary,
    event: "COMMENT",
  });

  console.log(
    `Handling PR ${payload.pull_request.number} for ${payload.repository.full_name}`
  );
};

const handlePullRequestSummary = async (payload, installationId) => {
  const response = await turtle.summarise(payload);
  const octokit = createOctokit(installationId);
  // Implement your PR handling logic here
  octokit.pulls.createComment({
    owner: payload.repository.owner.login,
    repo: payload.repository.name,
    pull_number: payload.pull_request.number,
    body: response.summary,
    event: "COMMENT",
  });

  console.log(
    `Handling PR ${payload.pull_request.number} for ${payload.repository.full_name}`
  );
};

const handleInstallation = async (payload) => {
  // Implement your installation handling logic here
  console.log(`New installation: ${payload.installation.id}`);
};

const handleIssue = async (payload, installationId) => {
  const octokit = createOctokit(installationId);
  console.log(
    `Handling issue ${payload.issue.number} for ${payload.repository.full_name}`
  );
  await octokit.issues.createComment({
    owner: payload.repository.owner.login,
    repo: payload.repository.name,
    issue_number: payload.issue.number,
    body: "Bot comment",
  });
};

export {
  handlePullRequestSummary,
  handlePullRequestReview,
  handleInstallation,
  handleIssue,
};
