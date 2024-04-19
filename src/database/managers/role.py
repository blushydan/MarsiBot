from abc import ABC, abstractmethod, abstractstaticmethod
from typing import Union

from src.database.tables import NormalRoles, GhostRoles
from src.database import DatabaseConnector as Connector


class RoleManager(ABC):
    @staticmethod
    @abstractmethod
    async def _get_role_object(user_id: str, ) -> Union[NormalRoles, GhostRoles]:
        pass

    @classmethod
    async def create_role(cls, user_id: int, role_id: int) -> None:
        async with Connector.get_session() as session:
            role = cls._get_role_object(user_id=user_id, role_id=role_id)
            session.add(role)

    @staticmethod
    async def get_role(user_id: int) -> NormalRoles:
        async with Connector.get_session() as session:
            role = await session.get(NormalRoles, user_id)
            return role

    @staticmethod
    async def update_role(user_id: int, **kwargs) -> None:
        async with Connector.get_session() as session:
            role = await session.get(NormalRoles, user_id)
            for key, value in kwargs.items():
                setattr(role, key, value)

    @staticmethod
    async def delete_role(user_id: int) -> None:
        async with Connector.get_session() as session:
            role = await session.get(NormalRoles, user_id)
            session.delete(role



class NormalRoleManager(RoleManager):
    ...


class GhostRoleManager(RoleManager):
    ...