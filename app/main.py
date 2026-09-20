from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.persons import router as persons_router
from app.db.session import engine, get_db_session


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()


app = FastAPI(
    title="Person Service",
    version="1.0.0",
    description="REST API for managing people",
    lifespan=lifespan,
)
app.include_router(persons_router, prefix="/api/v1")


@app.get("/health", tags=["System"])
async def health(
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    await session.execute(text("SELECT 1"))
    return {"status": "ok"}
