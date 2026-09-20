from fastapi import FastAPI

from app.api.persons import router as persons_router


app = FastAPI(
    title="Person Service",
    version="1.0.0",
    description="REST API for managing people",
)
app.include_router(persons_router, prefix="/api/v1")


@app.get("/health", tags=["System"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
