from typing import Any

from sqladmin import ModelView
from starlette.requests import Request

from src.apps.admin.exception import InvalidAdminUserDataError
from src.data_access.models import UserModel
from src.domain.user.dtos import UserInputDto
from src.domain.user.mappers import UserDomainMapper


class UserAdmin(ModelView, model=UserModel):
    column_list = [
        UserModel.id,
        UserModel.email,
        UserModel.first_name,
        UserModel.last_name,
        UserModel.is_active,
    ]
    column_details_list = [
        UserModel.id,
        UserModel.email,
        UserModel.first_name,
        UserModel.last_name,
        UserModel.is_active,
        UserModel.is_superuser,
        UserModel.created_at,
    ]
    column_searchable_list = [UserModel.email, UserModel.first_name, UserModel.last_name]
    column_sortable_list = [UserModel.email, UserModel.created_at]
    form_columns = [
        UserModel.email,
        UserModel.first_name,
        UserModel.last_name,
        UserModel.password,
        UserModel.is_active,
        UserModel.is_superuser,
    ]

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        """Perform some actions before a model is created or updated.
        By default does nothing.
        """
        try:
            dto = UserInputDto(**data)
            UserDomainMapper.input_dto_to_entity(dto)
        except Exception as e:
            raise InvalidAdminUserDataError(message=f'Введенные в адмике данные пользователя не валидны: {str(e)}')
