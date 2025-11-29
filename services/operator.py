from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import Operator
from schemas.operator import OperatorSchema, OperatorCreateSchema
from .contact_service import DistributionService


class OperatorService:
    @staticmethod
    async def create_operator(db: AsyncSession, operator_data: OperatorCreateSchema) -> OperatorSchema:
        db_operator = Operator(**operator_data.dict())
        db.add(db_operator)
        await db.commit()
        await db.refresh(db_operator)
        return OperatorSchema.from_orm(db_operator)

    @staticmethod
    async def get_all_operators(db: AsyncSession) -> List[OperatorSchema]:
        result = await db.execute(select(Operator))
        operators = result.scalars().all()

        result_list = []
        for operator in operators:
            operator_data = OperatorSchema.from_orm(operator)
            operator_data.current_load = await DistributionService.get_operator_load(db, operator.id)
            result_list.append(operator_data)
        return result_list
