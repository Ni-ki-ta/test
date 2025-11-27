from typing import List

from fastapi import APIRouter
from sqlalchemy import select

from services.service import DistributionService
from shemas.operator import OperatorSchema, OperatorCreateSchema
from src.models import Operator
from src.database import DBSession

operator_router = APIRouter(prefix="/operators", tags=["operators"])


@operator_router.post("/", response_model=OperatorSchema)
async def create_operator(
        operator: OperatorCreateSchema,
        db: DBSession
):
    db_operator = Operator(**operator.dict())
    db.add(db_operator)
    await db.commit()
    await db.refresh(db_operator)
    return db_operator


@operator_router.get("/", response_model=List[OperatorSchema])
async def list_operators(
        db: DBSession
):
    result = await db.execute(select(Operator))
    operators = result.scalars().all()

    result_list = []
    for operator in operators:
        operator_data = OperatorSchema.from_orm(operator)
        operator_data.current_load = await DistributionService.get_operator_load(db, operator.id)
        result_list.append(operator_data)
    return result_list
