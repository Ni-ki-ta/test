from typing import List
from fastapi import APIRouter

from schemas.lead import LeadSchema
from services import LeadService
from src.database import DBSession

lead_router = APIRouter(prefix="/contact", tags=["contact"])


@lead_router.get("/", response_model=List[LeadSchema])
async def list_leads(db: DBSession):
    return await LeadService.get_all_leads(db)
