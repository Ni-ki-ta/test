from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LeadBaseSchema(BaseModel):
    external_id: str
    email: Optional[str] = None
    phone: Optional[str] = None


class LeadCreateSchema(LeadBaseSchema):
    pass


class LeadSchema(LeadBaseSchema):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
