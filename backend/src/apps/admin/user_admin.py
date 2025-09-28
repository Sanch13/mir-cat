from sqladmin import ModelView

from src.data_access.models import UserModel


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
