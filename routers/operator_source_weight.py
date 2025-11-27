from fastapi import APIRouter

from shemas.operator_source_weight import OperatorSourceWeightSchema, OperatorSourceWeightCreateSchema
from src.database import DBSession
from src.models import OperatorSourceWeight

operator_source_weight_router = APIRouter(prefix="/operator_source_weight", tags=["operator_source_weight"])


@operator_source_weight_router.post("/", response_model=OperatorSourceWeightSchema)
async def create_weight(
        weight: OperatorSourceWeightCreateSchema,
        db: DBSession
):
    db_weight = OperatorSourceWeight(**weight.dict())
    db.add(db_weight)
    await db.commit()
    await db.refresh(db_weight)
    return db_weight
