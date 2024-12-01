import { Octokit } from "@octokit/rest";
import { createAppAuth } from "@octokit/auth-app";
import config from "../constants/config.js";
import { turtle } from "./turtle.service.js";
import fs from "fs";

const createOctokit = (installationId) =>
  new Octokit({
    authStrategy: createAppAuth,
    auth: {
      appId: config.GITHUB_APP_ID,
      privateKey: config.GITHUB_PRIVATE_KEY,
      installationId: installationId, // different for each installation , should be saved in database
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
  const octokit = createOctokit(installationId);
  const res = await octokit.pulls.get({
    owner: payload.repository.owner.login,
    repo: payload.repository.name,
    pull_number: payload.pull_request.number,
    mediaType: {
      format: "diff",
    },
  });
  // console.log(res.data);
  const response = await turtle.summerize(res.data);

  const body = `## Walkthrough\n\n${response.data.walkthrough}\n\n## Tabular Summary\n\n${response.data.tabular_summary}`;

  await octokit.pulls.createReview({
    owner: payload.repository.owner.login,
    repo: payload.repository.name,
    pull_number: payload.pull_request.number,
    body: body,
    event: "COMMENT",
  });

  console.log(
    `Handling PR ${payload.pull_request.number} for ${payload.repository.full_name}`
  );
};

const handleInstallation = async (payload) => {
  // Implement your installation handling logic here
  console.log(`New installation: ${payload.installation.id}`);
  // list all repositories for the installation
  const octokit = createOctokit(payload.installation.id);
  const { data } = await octokit.apps.listReposAccessibleToInstallation();
  console.log(data);
  await Promise.all(data.repositories.map((repo) => listAllContent(octokit, repo)));
};

const listAllContent = async (octokit, repo) => {
  const contents = await octokit.repos.getContent({
    owner: repo.owner.login,
    repo: repo.name,
  });
  const res = contents.data.forEach(async (content) => {
    const val = {
      repo: repo.name,
      action: "ADD",
      contents: [
        {
          name: content.name,
          path: content.path,
          type: content.type,
          code: await fetchFileContentFromDownloadUrl(content.download_url),
        },
      ],
    };
    console.log(val);
    return val;
  });
  console.log(res);
};

const fetchFileContentFromDownloadUrl = async (downloadUrl) => {
  const response = await fetch(downloadUrl);
  return response.text();
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
