from typing import List

from fastapi import APIRouter
from sqlalchemy import select

from shemas.lead import LeadSchema
from src.models import Lead
from src.database import DBSession

lead_router = APIRouter(prefix="/contact", tags=["contact"])


@lead_router.get("/", response_model=List[LeadSchema])
async def list_leads(db: DBSession):
    result = await db.execute(select(Lead))
    leads = result.scalars().all()
    return leads
