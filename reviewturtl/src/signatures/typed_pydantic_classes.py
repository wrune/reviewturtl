from pydantic import BaseModel
from typing import Optional

class ReviewComments(BaseModel):
    line_range: str
    suggested_code_change: Optional[str] = None
    comment: Optional[str] = None
