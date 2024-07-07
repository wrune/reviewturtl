from pydantic import BaseModel
from typing import Optional, Any


class SummarizerRequest(BaseModel):
    file_diff: str
    context: Optional[str] = None


class SummarizerData(BaseModel):
    reason: str
    walkthrough: str
    tabular_summary: str


class SummarizerResponse(BaseModel):
    error: Optional[str] = None
    data: Optional[SummarizerData] = None
    meta: Optional[Any] = None
