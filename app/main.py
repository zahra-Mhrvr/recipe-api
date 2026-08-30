from fastapi import FastAPI

from app.database import Base, engine
from app.routers import recipes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Recipe Finder API",
    description="Small API for storing recipes and searching by ingredient.",
    version="0.1.0",
)

app.include_router(recipes.router)


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}
