from fastapi import FastAPI

from routers.routers import api_router


def create_app() -> FastAPI:
    application = FastAPI()

    application.include_router(router=api_router, prefix="/api")

    return application


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
