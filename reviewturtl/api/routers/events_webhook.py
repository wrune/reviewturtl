from fastapi import APIRouter, Request, HTTPException, status
import httpx
from reviewturtl.logger import get_logger
from reviewturtl.settings import get_settings

settings = get_settings()
log = get_logger(__name__)
router = APIRouter()

SUMMARIZE_ENDPOINT = (
    "http://localhost:8000/api/v1/summarize"  # Update with actual endpoint
)


async def fetch_diff_content(diff_url: str, token: str) -> str:
    headers = {"Authorization": f"token {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(diff_url, headers=headers)
        response.raise_for_status()
        return response.text


async def call_summarizer(file_diff: str, request_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SUMMARIZE_ENDPOINT,
            json={"file_diff": file_diff},
            headers={"X-Request-ID": request_id},
        )
        response.raise_for_status()
        return response.json()


async def post_github_comment(pr_number: int, comment: str, repo: str, token: str):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"body": comment}, headers=headers)
        response.raise_for_status()


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
        log.debug(f"Payload: {payload}")
        payload = payload.get("payload", {})
        action = payload.get("action")
        pr_number = payload.get("number")
        pr_title = payload.get("pull_request", {}).get("title")
        repo = payload.get("repository", {}).get("full_name")
        request_id = request.headers.get("X-Request-ID", "default-request-id")
        diff_url = payload.get("pull_request", {}).get("diff_url")
        body = payload.get("pull_request", {}).get("body")
        github_token = settings.PAT_TOKEN
        log.debug(f"Diff URL: {diff_url}")
        log.debug(f"Body: {body}")

        # Fetch diff content
        file_diff = await fetch_diff_content(diff_url, github_token)
        log.debug(f"File Diff Content: {file_diff}")

        # Call summarizer endpoint
        summary_response = await call_summarizer(file_diff, request_id)
        summary = summary_response.get("data", {}).get(
            "walkthrough", "No summary available"
        )

        # Post comment on GitHub PR
        comment = f"Summary of changes:\n\n{summary}"
        await post_github_comment(pr_number, comment, repo, github_token)

        log.info(f"Pull Request #{pr_number} {action}: {pr_title}")
    elif event == "push":
        # Handle push event
        log.info(f"Push event received with payload: {payload}")
        # Add your push event handling logic here
    else:
        # Handle other events if necessary
        log.warning(f"Unhandled event: {event}")

    return {"detail": "Webhook processed successfully"}
