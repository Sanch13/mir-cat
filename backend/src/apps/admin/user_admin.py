from crudadmin import CRUDAdmin
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.amis.components import PageSchema
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


class UserAmisAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label="Пользователи", icon="fa fa-users")
    model = UserModel
    list_display = [
        UserModel.id,
        UserModel.email,
        UserModel.first_name,
        UserModel.last_name,
        UserModel.is_active,
        UserModel.created_at,
    ]
    search_fields = [UserModel.email, UserModel.first_name, UserModel.last_name]
    list_filter = [UserModel.is_active, UserModel.is_superuser, UserModel.created_at]

    # Настройка форм
    async def get_form(self, request):
        form = await super().get_form(request)
        form.body.sort = False  # Отключаем сортировку полей
        return form


class UserCRUDAdmin(CRUDAdmin):
    model = UserModel
    list_display = ["id", "email", "first_name", "last_name", "is_active", "created_at"]
    search_fields = ["email", "first_name", "last_name"]
    list_filter = ["is_active", "is_superuser", "created_at"]
    ordering = ["-created_at"]

    # Настройка полей формы
    form_fields = ["email", "first_name", "last_name", "password", "is_active", "is_superuser"]
