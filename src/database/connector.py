from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import SQLAlchemyError


class DatabaseConnector:
    """Static class to manage the database connection"""
    # Private class variables
    _engine = None
    _async_session = None

    @staticmethod
    def initialize(database_url: str, echo: bool = False):
        """Static method to initialize the database connection"""
        if DatabaseConnector._engine is not None:
            raise Exception("DatabaseConnector is already initialized.")

        DatabaseConnector._engine = create_async_engine(
            database_url,
            echo=echo,  # Echo can be enabled for debugging
            future=True
        )

        DatabaseConnector._async_session = sessionmaker(
            DatabaseConnector._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @staticmethod
    async def get_session():
        """Static method to get the session, use 'async with' for context management"""
        if DatabaseConnector._async_session is None:
            raise Exception("DatabaseConnector is not initialized. Call 'initialize' first.")

        async with DatabaseConnector._async_session() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

