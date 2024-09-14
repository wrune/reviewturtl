from fastapi import APIRouter, Request, HTTPException, status
from reviewturtl.logger import get_logger
from reviewturtl.settings import get_settings
from reviewturtl.clients.github_client import (
    fetch_diff_content,
    post_github_comment,
    update_github_comment,
    get_existing_comment,
)
from reviewturtl.clients.ai_client import call_summarizer
import json

settings = get_settings()
log = get_logger(__name__)
router = APIRouter()

COMMENT_IDENTIFIER = "AI_SUMMARY_COMMENT"


@router.post("/api/v1/github_webhook", status_code=status.HTTP_204_NO_CONTENT)
async def github_webhook(request: Request):
    # Log request headers for debugging
    log.debug(f"Request headers: {request.headers}")

    # Verify the request is from GitHub
    content_type = request.headers.get("content-type")
    if content_type == "application/json":
        payload = await request.json()
    elif content_type == "application/x-www-form-urlencoded":
        form_data = await request.form()
        payload = {key: value for key, value in form_data.items()}
    else:
        log.error(f"Invalid content-type: {content_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid payload: content-type must be application/json or application/x-www-form-urlencoded, got {content_type}",
        )

    event = request.headers.get("X-GitHub-Event", "ping")
    log.debug(f"Received event: {event}")

    if event == "pull_request":
        # Log the payload
        log.debug(f"Payload: {payload}")
        payload = json.loads(payload.get("payload", {}))
        action = payload.get("action")
        pr_number = payload.get("number")
        pr_title = payload.get("pull_request", {}).get("title")
        repo_full_name = payload.get("repository", {}).get("full_name")
        request_id = request.headers.get("X-Request-ID", "default-request-id")
        diff_url = payload.get("pull_request", {}).get("diff_url")
        body = payload.get("pull_request", {}).get("body")
        github_token = settings.PAT_TOKEN
        owner, repo = repo_full_name.split("/")
        log.debug(f"Diff URL: {diff_url}")
        log.debug(f"Body: {body}")

        # Fetch diff content
        file_diff = await fetch_diff_content(owner, repo, pr_number, github_token)
        log.debug(f"File Diff Content: {file_diff}")

        # Call summarizer endpoint
        summary_response = await call_summarizer(file_diff, request_id)
        summary = summary_response.get("data", {}).get(
            "walkthrough", "No summary available"
        )
        tabular_summary = summary_response.get("data", {}).get(
            "tabular_summary", "No tabular summary available"
        )

        comment_body = f"### AI Summary of Changes\n\n{summary}\n\n**Tabular Summary:**\n\n{tabular_summary}"
        comment_body_with_id = f"{COMMENT_IDENTIFIER}\n\n{comment_body}"

        if action == "opened":
            # Post new comment
            comment = await post_github_comment(
                pr_number, comment_body_with_id, owner, repo, github_token
            )
            log.info(f"Posted new comment to PR #{pr_number}: {comment['id']}")
        elif action in ["synchronize", "edited"]:
            # Fetch existing comment
            existing_comment = await get_existing_comment(
                pr_number, owner, repo, github_token, identifier=COMMENT_IDENTIFIER
            )
            if existing_comment:
                # Update existing comment
                updated_comment = await update_github_comment(
                    existing_comment["id"], comment_body, owner, repo, github_token
                )
                log.info(
                    f"Updated comment {existing_comment['id']} on PR #{pr_number} with {updated_comment['body']}"
                )
            else:
                # If no existing comment, post a new one
                comment = await post_github_comment(
                    pr_number, comment_body_with_id, owner, repo, github_token
                )
                log.info(f"Posted new comment to PR #{pr_number}: {comment['id']}")
        else:
            log.warning(f"Unhandled pull_request action: {action}")

        log.info(f"Pull Request #{pr_number} {action}: {pr_title}")
    elif event == "push":
        # Handle push event
        log.info(f"Push event received with payload: {payload}")
        # Add your push event handling logic here
    else:
        # Handle other events if necessary
        log.warning(f"Unhandled event: {event}")

    return {"detail": "Webhook processed successfully"}
