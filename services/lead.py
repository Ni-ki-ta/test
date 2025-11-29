from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import Lead
from schemas.lead import LeadSchema


class LeadService:
    @staticmethod
    async def get_all_leads(db: AsyncSession) -> List[LeadSchema]:
        result = await db.execute(select(Lead))
        leads = result.scalars().all()
        return [LeadSchema.from_orm(lead) for lead in leads]