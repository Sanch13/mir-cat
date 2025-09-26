import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.user.irepo import IUserRepository
from src.data_access.mappers.user_mapper import UserMapper

from src.data_access.models import UserModel
from src.domain.user.entity import UserEntity


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = UserModel

    async def save(self, user: UserEntity) -> None:
        user_model = UserMapper.entity_to_model(user)
        self._session.add(user_model)

    async def get_by_id(self, user_id: UUID) -> UserEntity | None:
        query = select(self.model).where(self.model.id == user_id)
        result = await self._session.execute(query)
        sql_user = result.scalar_one_or_none()
        return UserMapper.model_to_entity(sql_user) if sql_user else None