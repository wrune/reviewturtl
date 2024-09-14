from fastapi import APIRouter, Request, HTTPException, status
from reviewturtl.logger import get_logger
from reviewturtl.src.event_utils.pr_scrutnizer import pr_action_handler

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
        await pr_action_handler(payload, request)
    elif event == "push":
        # Handle push event
        log.info(f"Push event received with payload: {payload}")
        # Add your push event handling logic here
    else:
        # Handle other events if necessary
        log.warning(f"Unhandled event: {event}")

    return {"detail": "Webhook processed successfully"}
