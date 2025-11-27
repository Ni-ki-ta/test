from typing import Optional

from pydantic import BaseModel


class SourceBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None


class SourceCreateSchema(SourceBaseSchema):
    pass


class SourceSchema(SourceBaseSchema):
    id: int

    class Config:
        from_attributes = True
        