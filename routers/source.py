from typing import List
from fastapi import APIRouter

from schemas.source import SourceSchema, SourceCreateSchema
from services import SourceService
from src.database import DBSession

source_router = APIRouter(prefix="/sources", tags=["sources"])


@source_router.post("/", response_model=SourceSchema)
async def create_source(
        source: SourceCreateSchema,
        db: DBSession
):
    return await SourceService.create_source(db, source)


@source_router.get("/", response_model=List[SourceSchema])
async def list_sources(
        db: DBSession
):
    return await SourceService.get_all_sources(db)
