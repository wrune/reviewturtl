from reviewturtl.logger import get_logger
import json
from reviewturtl.settings import get_settings
from reviewturtl.clients.github_client import fetch_diff_content
from reviewturtl.clients.ai_client import call_summarizer
from reviewturtl.clients.github_client import (
    post_github_comment,
    update_github_comment,
    get_existing_comment,
)

# A specific identifier for the comment
COMMENT_IDENTIFIER = "AI Summary of Changes"
settings = get_settings()

log = get_logger(__name__)


async def process_payload(payload, request):
    # Log the payload
    log.debug(f"Payload: {payload}")
    # check what payload is required
    payload = json.loads(payload.get("payload", {}))
    # action of the PR
    action = payload.get("action")
    # get the PR number
    pr_number = payload.get("number")
    # get the PR title
    pr_title = payload.get("pull_request", {}).get("title")
    # get the repo full name
    repo_full_name = payload.get("repository", {}).get("full_name")
    # get the request id
    request_id = request.headers.get("X-Request-ID", "default-request-id")
    # get the diff url
    diff_url = payload.get("pull_request", {}).get("diff_url")
    # get the PR body
    body = payload.get("pull_request", {}).get("body")
    # get the PR url
    github_token = settings.PAT_TOKEN
    # get the owner and repo
    owner, repo = repo_full_name.split("/")

    log.debug(f"Diff URL: {diff_url}")
    log.debug(f"Body: {body}")

    # Fetch diff content
    file_diff = await fetch_diff_content(owner, repo, pr_number, github_token)
    log.debug(f"File Diff Content: {file_diff}")

    return {
        "action": action,
        "pr_number": pr_number,
        "pr_title": pr_title,
        "repo_full_name": repo_full_name,
        "request_id": request_id,
        "diff_url": diff_url,
        "body": body,
        "github_token": github_token,
        "owner": owner,
        "repo": repo,
        "file_diff": file_diff,
    }


async def pr_action_handler(payload, request):
    event_data = await process_payload(payload, request)
    # get the data from the event_data
    file_diff = event_data.get("file_diff")
    request_id = event_data.get("request_id")
    action = event_data.get("action")
    pr_number = event_data.get("pr_number")
    owner = event_data.get("owner")
    repo = event_data.get("repo")
    github_token = event_data.get("github_token")
    # pr_title = event_data.get("pr_title")
    # Call summarizer endpoint
    summary_response = await call_summarizer(file_diff, request_id)
    summary = summary_response.get("data", {}).get(
        "walkthrough", "No summary available"
    )
    tabular_summary = summary_response.get("data", {}).get(
        "tabular_summary", "No tabular summary available"
    )
    # Construct the comment body
    comment_body = f"### {COMMENT_IDENTIFIER}\n\n{summary}\n\n**Tabular Summary:**\n\n{tabular_summary}"

    if action == "opened":
        # Post new comment
        comment = await post_github_comment(
            pr_number, comment_body, owner, repo, github_token
        )
        log.debug(f"Posted new comment to PR #{pr_number} with {comment}")
    elif action in ["synchronize", "edited"]:
        # Fetch existing comment
        existing_comment = await get_existing_comment(
            pr_number, owner, repo, github_token, identifier=COMMENT_IDENTIFIER
        )
        if existing_comment:
            # Update existing comment with the identifier
            updated_comment = await update_github_comment(
                existing_comment["id"], comment_body, owner, repo, github_token
            )
            log.debug(
                f"Updated comment {existing_comment['id']} on PR #{pr_number} with {updated_comment['body']}"
            )
        else:
            # If no existing comment is found with the identifier, post a new one
            comment = await post_github_comment(
                pr_number, comment_body, owner, repo, github_token
            )
            log.debug(f"Posted new comment to PR #{pr_number} with {comment}")
    else:
        log.debug(f"No action required for PR #{pr_number}")
