from pydantic import BaseModel


class OperatorSourceWeightBaseSchema(BaseModel):
    operator_id: int
    source_id: int
    weight: int = 1


class OperatorSourceWeightCreateSchema(OperatorSourceWeightBaseSchema):
    pass


class OperatorSourceWeightSchema(OperatorSourceWeightBaseSchema):
    id: int

    class Config:
        from_attributes = True
        