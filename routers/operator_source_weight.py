from fastapi import APIRouter

from schemas.operator_source_weight import OperatorSourceWeightSchema, OperatorSourceWeightCreateSchema
from services import OperatorSourceWeightService
from src.database import DBSession

operator_source_weight_router = APIRouter(prefix="/operator_source_weight", tags=["operator_source_weight"])


@operator_source_weight_router.post("/", response_model=OperatorSourceWeightSchema)
async def create_weight(
        weight: OperatorSourceWeightCreateSchema,
        db: DBSession
):
    return await OperatorSourceWeightService.create_weight(db, weight)
