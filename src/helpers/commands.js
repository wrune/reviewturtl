import lodash from "lodash"
import { handlePullRequestReview, handlePullRequestSummary } from "../services/octokit.service.js";
import { PullRequest } from "./pullRequests.js";

const commands = {
    FULL_REVIEW: "full review",
    PAUSE: "pause",
    REVIEW: "review",
    RESUME: "resume",
    SUMMARY: "summary",
    RESOLVE: "resolve",
    CONFIG: "configuration",
    HELP: "help"
}

export class Command {
    isCommand = false;
    command = null;
    body = null;
    installationId = "";
    pr = new PullRequest();

    constructor(body, installationId) {
        this.body = body;
        this.installationId = installationId;

        if (body?.comment?.body.includes("@reviewturtl")) {
            const comment = lodash.words(body?.comment?.body).join(" ");
            const command = Object.keys(commands).find((command) => comment.includes(`@reviewturtl ${commands[command]}`));
            if (command) {
                this.isCommand = true;
                this.command = command;
                this.pr = new PullRequest(body);
            }
        }
    }

    async fullReview() {
        await handlePullRequestReview(this.body, this.installationId);
    }

    async summary() {
        await handlePullRequestSummary(this.body, this.installationId);
    }

    async pause() {
        await this.pr.deactivate();
    }

    async resume() {
        await this.pr.activate();
    }
}