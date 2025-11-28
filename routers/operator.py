from typing import List
from fastapi import APIRouter

from services import OperatorService
from schemas.operator import OperatorSchema, OperatorCreateSchema
from src.database import DBSession

operator_router = APIRouter(prefix="/operators", tags=["operators"])


@operator_router.post("/", response_model=OperatorSchema)
async def create_operator(
        operator: OperatorCreateSchema,
        db: DBSession
):
    return await OperatorService.create_operator(db, operator)


@operator_router.get("/", response_model=List[OperatorSchema])
async def list_operators(
        db: DBSession
):
    return await OperatorService.get_all_operators(db)
