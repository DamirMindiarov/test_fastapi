from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

# DATABASE_URL = "sqlite+aiosqlite:///./database.db"
DATABASE_URL = "sqlite+aiosqlite:///path/database.db"

engine = create_async_engine(DATABASE_URL, echo=True)
session = async_sessionmaker(engine, expire_on_commit=False)()
