from fastapi import APIRouter, Request, HTTPException, status
from reviewturtl.logger import get_logger

log = get_logger(__name__)
router = APIRouter()


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
