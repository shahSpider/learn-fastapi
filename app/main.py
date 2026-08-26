from fastapi import FastAPI
from app.books.routes import book_router
from contextlib import asynccontextmanager
from app.db.database import init_db

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is starting...")
    await init_db()
    yield
    print(f"Server has been stopped!")

version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version,
    lifespan=life_span
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])

@app.get("/")
async def read_root():
    return {"message": "Hello World"}