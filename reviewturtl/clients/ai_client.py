import httpx

# summarize endpoint
SUMMARIZE_ENDPOINT = (
    "http://localhost:7001/api/v1/summarize"  # Update with actual endpoint
)


async def call_summarizer(file_diff: str, request_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SUMMARIZE_ENDPOINT,
            json={"file_diff": file_diff},
            headers={"X-Request-ID": request_id},
        )
        response.raise_for_status()
        return response.json()
