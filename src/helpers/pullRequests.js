import db from "../db/prisma.client.js";

export class PullRequest {
    pull_request = null;

    constructor(body) {
        this.pull_request = {
            pr_number: body?.pull_request?.number,
            repo_name: body?.repository?.name,
            owner: body?.organization?.login,
            installation_id: body?.installation?.id
        }
    }

    async active() {
        try {
            const result = await db.pull_requests.findFirst({
                where: {
                    pr_number: this.pull_request.pr_number,
                    repo_name: this.pull_request.repo_name,
                    owner: this.pull_request.owner,
                    turtle_status: "ACTIVE"
                }
            });

            if (!result || result.turtle_status === "ACTIVE") {
                return true;
            }

            return false;
        } catch (error) { }
    }

    async exists() {
        try {
            const result = await db.pull_requests.findFirst({
                where: {
                    pr_number: this.pull_request.pr_number,
                    repo_name: this.pull_request.repo_name,
                    owner: this.pull_request.owner
                }
            });

            console.log(result);

            return result;
        } catch (error) {
            console.error(error);
        }
    }

    async save() {
        try {
            const exists = await this.exists();

            if (!exists) {
                console.log("Created!");
                await db.pull_requests.create({ data: this.pull_request });
            }
        } catch (error) {
            console.error(error);
        }
    }

    async activate() {
        try {
            await db.pull_requests.update({
                where: { pr_number: this.pull_request.pr_number },
                data: { turtle_status: "ACTIVE" }
            });
        } catch (error) {
            console.error(error);
        }
    }

    async deactivate() {
        try {
            await db.pull_requests.update({
                where: { pr_number: this.pull_request.pr_number },
                data: { turtle_status: "INACTIVE" }
            });
        } catch (error) {
            console.error(error);
        }
    }
}