from uuid import UUID

import structlog
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.user.irepo import IUserRepository
from src.domain.user.entity import UserEntity
from src.infrastructure.data_access.models import UserModel
from src.infrastructure.data_access.users.mapper import UserModelMapper
from src.infrastructure.exception_decorator import handle_db_errors

logger = structlog.get_logger()


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = UserModel

    @handle_db_errors
    async def save(self, user: UserEntity) -> None:
        logger.debug("saving_user_to_db", user_id=str(user.id))
        user_model = UserModelMapper.entity_to_model(user)
        self._session.add(user_model)

    @handle_db_errors
    async def get_by_id(self, user_id: UUID) -> UserEntity | None:
        query = select(self.model).where(self.model.id == user_id)
        result = await self._session.execute(query)
        sql_user = result.scalar_one_or_none()
        return UserModelMapper.model_to_entity(sql_user) if sql_user else None

    @handle_db_errors
    async def get_by_email(self, email: str) -> UserEntity | None:
        logger.debug("fetching_user_by_email", email=email)
        query = select(self.model).where(self.model.email == email.lower())
        result = await self._session.execute(query)
        sql_user = result.scalar_one_or_none()

        if not sql_user:
            logger.debug("user_not_found_in_db", email=email)

        return UserModelMapper.model_to_entity(sql_user) if sql_user else None

    @handle_db_errors
    async def email_exists(self, email: str) -> bool:
        stmt = select(exists().where(self.model.email == email))
        result = await self._session.execute(stmt)
        return result.scalar()
