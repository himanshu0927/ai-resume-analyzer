import datetime
from pydantic import BaseModel
from typing import Optional, List, Any

class ResumeResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    file_type: str
    uploaded_at: datetime.datetime

    class Config:
        from_attributes = True

class ResumeDetailResponse(ResumeResponse):
    extracted_text: Optional[str] = None
