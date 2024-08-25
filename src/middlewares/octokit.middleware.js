import { Octokit } from "@octokit/rest";
import { createAppAuth } from "@octokit/auth-app";
import config from "../constants/config.js";

async function createOctokitClient(installationId) {
  return new Octokit({
    authStrategy: createAppAuth,
    auth: {
      appId: config.GITHUB_APP_ID,
      privateKey: config.GITHUB_PRIVATE_KEY,
      installationId: installationId,
    },
  });
}

async function octokitMiddleware(req, res, next) {
  const installationId = req.body.installation?.id;
  req.octokit = await createOctokitClient(installationId);
  next();
}

export { octokitMiddleware };
