from crudadmin import CRUDAdmin
from fastapi_amis_admin.admin import AdminSite, Settings
from pydantic import BaseModel
from sqladmin import Admin
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.apps.admin.user_admin import UserAdmin, UserAmisAdmin
from src.config import db_settings
from src.data_access.models import UserModel

engine = create_engine(
    url=db_settings.construct_sync_sqlalchemy_url,
)

# Создайте engine и sessionmaker прямо в этом файле
a_engine = create_async_engine(db_settings.construct_sqlalchemy_url)
sessionmaker = async_sessionmaker(bind=a_engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with sessionmaker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Простые схемы для CRUDAdmin
class UserCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str
    password: str
    is_superuser: bool = False
    is_active: bool = True


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    is_superuser: bool | None = None
    is_active: bool | None = None


def make_sql_admin(app):
    # Создаем админку
    admin = Admin(app, engine, base_url="/sql-admin")
    admin.add_view(UserAdmin)


def make_amis_admin(app):
    settings = Settings()
    settings.site_path = "/amis-admin"
    # Создаем админку
    admin_site = AdminSite(settings=settings, engine=engine)

    admin_site.register_admin(UserAmisAdmin)

    # Монтируем админку к приложению
    admin_site.mount_app(app)


def make_crud_admin(app):
    # Создаем админку
    crud_admin = CRUDAdmin(
        session=get_session,
        SECRET_KEY="asdasd",  # pragma: allowlist secret
    )
    crud_admin.add_view(
        model=UserModel,
        create_schema=UserCreate,
        update_schema=UserUpdate,
        allowed_actions={"view", "create", "update", "delete"},
    )
    app.mount("/crud-admin", crud_admin.app)
