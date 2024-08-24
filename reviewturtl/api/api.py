from fastapi import FastAPI
from reviewturtl.settings import get_settings, initialize_dspy_with_configs
from reviewturtl.api.routers import summarizer, reviewer, code_search, index_code

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
app.include_router(code_search.router)
app.include_router(index_code.router)
