from fastapi import FastAPI
from sqlalchemy import text

from routers.routers import api_router
from src.database import async_engine, Base


async def check_and_create_tables():
    required_tables = ['operators', 'leads', 'sources', 'operator_source_weights', 'contacts']
    missing_tables = []

    async with async_engine.connect() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        existing_tables = [row[0] for row in result.fetchall()]

        for table in required_tables:
            if table not in existing_tables:
                missing_tables.append(table)

    if missing_tables:
        print(f"Missing tables: {missing_tables}, creating...")
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")
        return True
    else:
        print("All tables exist, skipping creation.")
        return False


def create_app() -> FastAPI:
    application = FastAPI()

    @application.on_event("startup")
    async def startup_event():
        await check_and_create_tables()

    application.include_router(router=api_router, prefix="/api")

    return application


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
