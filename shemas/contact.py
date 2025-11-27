from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from shemas.operator import OperatorSchema


class ContactBaseSchema(BaseModel):
    lead_external_id: str
    source_id: int
    message: Optional[str] = None


class ContactCreateSchema(ContactBaseSchema):
    pass


class ContactSchema(ContactBaseSchema):
    id: int
    lead_id: int
    operator_id: Optional[int]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ContactResponseSchema(BaseModel):
    contact: ContactSchema
    operator: Optional[OperatorSchema] = None
