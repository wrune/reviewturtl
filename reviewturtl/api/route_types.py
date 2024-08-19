from pydantic import BaseModel
from typing import Optional, Any, List, Union, Dict
from reviewturtl.src.signatures.signatures import ReviewComments


class SummarizerRequest(BaseModel):
    file_diff: str
    context: Optional[str] = None


class ReviewerRequest(BaseModel):
    file_diff: str
    file_content: Optional[str] = None
    context: Optional[str] = None


class SummarizerData(BaseModel):
    reason: str
    walkthrough: str
    tabular_summary: str


class ReviewerData(BaseModel):
    line_by_line_comments: List[ReviewComments]


class CodeSearchResponse(BaseModel):
    response_for_search_query: str


class CodeSearchRequest(BaseModel):
    search_query: str
    collection_name: str
    conversation_history: Dict[str, str]


class StandardResponse(BaseModel):
    error: Optional[str] = None
    data: Optional[Union[SummarizerData, ReviewerData, CodeSearchResponse]] = None
    meta: Optional[Any] = None
