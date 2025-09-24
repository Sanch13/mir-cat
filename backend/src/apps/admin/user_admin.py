from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import create_engine

from src.config.db_settings import db_settings
from src.data_access.models import UserModel

engine = create_engine(
    url=db_settings.construct_sqlalchemy_url(),
)

app = FastAPI()
admin = Admin(app, engine)


class UserAdmin(ModelView, model=UserModel):
    column_list = [UserModel.id, UserModel.first_name]


admin.add_view(UserAdmin)
