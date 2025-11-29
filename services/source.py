from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models import Source
from schemas.source import SourceSchema, SourceCreateSchema


class SourceService:
    @staticmethod
    async def create_source(db: AsyncSession, source_data: SourceCreateSchema) -> SourceSchema:
        existing_source = await SourceService._get_source_by_name(db, source_data.name)
        if existing_source:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Source with name '{source_data.name}' already exists"
            )

        db_source = Source(**source_data.dict())
        db.add(db_source)

        try:
            await db.commit()
            await db.refresh(db_source)
            return SourceSchema.from_orm(db_source)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Source with name '{source_data.name}' already exists"
            )

    @staticmethod
    async def get_all_sources(db: AsyncSession) -> List[SourceSchema]:
        result = await db.execute(select(Source))
        sources = result.scalars().all()
        return [SourceSchema.from_orm(source) for source in sources]

    @staticmethod
    async def _get_source_by_name(db: AsyncSession, name: str) -> Optional[Source]:
        result = await db.execute(select(Source).where(Source.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_source_by_id(db: AsyncSession, source_id: int) -> Optional[Source]:
        result = await db.execute(select(Source).where(Source.id == source_id))
        return result.scalar_one_or_none()
