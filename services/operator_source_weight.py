from sqlalchemy.ext.asyncio import AsyncSession
from src.models import OperatorSourceWeight
from schemas.operator_source_weight import OperatorSourceWeightSchema, OperatorSourceWeightCreateSchema


class OperatorSourceWeightService:
    @staticmethod
    async def create_weight(db: AsyncSession, weight_data: OperatorSourceWeightCreateSchema) -> OperatorSourceWeightSchema:
        db_weight = OperatorSourceWeight(**weight_data.dict())
        db.add(db_weight)
        await db.commit()
        await db.refresh(db_weight)
        return OperatorSourceWeightSchema.from_orm(db_weight)
