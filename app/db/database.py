from sqlmodel import text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import get_settings
from app.books.models import Book

settings = get_settings()

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True
)


async def init_db():
    async with engine.begin() as conn:
       print("Creating database tables...")
       await conn.run_sync(SQLModel.metadata.create_all) 