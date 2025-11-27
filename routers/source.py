from typing import List

from fastapi import APIRouter
from sqlalchemy import select

from shemas.source import SourceSchema, SourceCreateSchema
from src import models
from src.database import DBSession
from src.models import Source

source_router = APIRouter(prefix="/sources", tags=["sources"])


@source_router.post("/", response_model=SourceSchema)
async def create_source(
        source: SourceCreateSchema,
        db: DBSession
):
    db_source = models.Source(**source.dict())
    db.add(db_source)
    await db.commit()
    await db.refresh(db_source)
    return db_source


@source_router.get("/", response_model=List[SourceSchema])
async def list_sources(
        db: DBSession
):
    result = await db.execute(select(Source))
    sources = result.scalars().all()
    return sources
