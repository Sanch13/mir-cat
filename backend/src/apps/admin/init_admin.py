from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy import create_engine

from src.apps.admin.user_admin import UserAdmin
from src.config import all_settings as settings


def init_sql_admin(app: FastAPI) -> None:
    """Инициализация SQLAdmin"""
    engine = create_engine(url=settings.db.construct_sync_sqlalchemy_url)
    admin = Admin(app=app, engine=engine)

    admin.add_view(UserAdmin)
