from typing import Optional

from pydantic import BaseModel


class OperatorBaseSchema(BaseModel):
    name: str
    is_active: bool = True
    load_limit: int = 10


class OperatorCreateSchema(OperatorBaseSchema):
    pass


class OperatorSchema(OperatorBaseSchema):
    id: int
    current_load: Optional[int] = 0

    class Config:
        from_attributes = True
