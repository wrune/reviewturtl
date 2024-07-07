from fastapi import FastAPI
from reviewturtl.settings import get_settings
from reviewturtl.api.routers import summarizer

cfg = get_settings()

app = FastAPI()


@app.get("/api/health")
async def health():
    return {
        "status": "OK",
        "app_name": cfg.APP_NAME,
        "environment": cfg.ENVIRONMENT,
    }


app.include_router(summarizer.router)
