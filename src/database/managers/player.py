from src.database.tables import Players
from src.database import DatabaseConnector as Connector


class PlayerManager:
    @staticmethod
    async def create_player(user_id: int, username: str) -> None:
        async with Connector.get_session() as session:
            player = Players(user_id=user_id, username=username)
            session.add(player)

    @staticmethod
    async def get_player(user_id: int) -> Players:
        async with Connector.get_session() as session:
            player = await session.get(Players, user_id)
            return player

    @staticmethod
    async def update_player(user_id: int, **kwargs) -> None:
        async with Connector.get_session() as session:
            player = await session.get(Players, user_id)
            for key, value in kwargs.items():
                setattr(player, key, value)

    @staticmethod
    async def delete_player(user_id: int) -> None:
        async with Connector.get_session() as session:
            player = await session.get(Players, user_id)
            session.delete(player)


