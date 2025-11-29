import re
from typing import AsyncGenerator, Annotated, TypeAlias

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.config import settings


def camel_case_to_snake_case(camel_case_str):
    snake_case_str = re.sub(r'(?<!^)(?=[A-Z])', '_', camel_case_str).lower()
    return snake_case_str


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"


async_engine = create_async_engine(
    url=settings.async_database_url,
    echo=True
)

async_session = async_sessionmaker(async_engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


DBSession: TypeAlias = Annotated[AsyncSession, Depends(get_async_session)]
