from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session

from core.config import settings


class Database:
    def __init__(self, url: str):
        self.engine = create_async_engine(
            url=url,
            echo=True,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False, expire_on_commit=True
        )

    async def scoped_session_dependency(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        yield session
        await session.close()


database = Database(settings.db.url)
