from fastapi import FastAPI
from reviewturtl.settings import get_settings,initialize_dspy_with_configs
from reviewturtl.api.routers import summarizer,reviewer

cfg = get_settings()
initialize_dspy_with_configs()
app = FastAPI()



@app.get("/api/health")
async def health():
    return {
        "status": "OK",
        "app_name": cfg.APP_NAME,
        "environment": cfg.ENVIRONMENT,
    }


app.include_router(summarizer.router)
app.include_router(reviewer.router)

