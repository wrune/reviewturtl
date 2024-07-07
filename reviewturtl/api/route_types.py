from pydantic import BaseModel
from typing import Optional, Any


class SummarizerChunk(BaseModel):
    old_chunk_code: str
    new_chunk_code: str


class SummarizerRequest(BaseModel):
    chunks: SummarizerChunk
    context: Optional[str] = None


class SummarizerData(BaseModel):
    reason: str
    summary: str


class SummarizerResponse(BaseModel):
    error: Optional[str] = None
    data: Optional[SummarizerData] = None
    meta: Optional[Any] = None
