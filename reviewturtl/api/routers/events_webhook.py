from fastapi import APIRouter, Request, HTTPException, status


from reviewturtl.logger import get_logger
from typing import Any

log = get_logger(__name__)
router = APIRouter()


@router.post("/api/v1/github_webhook", status_code=status.HTTP_204_NO_CONTENT)
async def github_webhook(request: Request):
    # Verify the request is from GitHub
    if request.headers.get("content-type") != "application/json":
        log.error("Invalid content-type")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload"
        )

    event = request.headers.get("X-GitHub-Event", "ping")
    payload = await request.json()  # Corrected to parse JSON payload
    log.debug(f"Received event: {event}")

    if event == "pull_request":
        action = payload.get("action")
        pr_number = payload.get("number")
        pr_title = payload.get("pull_request", {}).get("title")

        if action == "opened":
            # Handle PR opened event
            log.info(f"Pull Request #{pr_number} opened: {pr_title}")
            # Add your summarization logic here
        elif action == "synchronize":
            # Handle PR updated with new commits
            log.info(f"Pull Request #{pr_number} synchronized with new commits.")
            # Update the summary as needed
        else:
            log.warning(f"Unhandled pull request action: {action}")
    else:
        # Handle other events if necessary
        log.warning(f"Unhandled event: {event}")

    return {"detail": "Webhook processed successfully"}
