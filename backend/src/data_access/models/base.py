from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from src.config.db_settings import db_settings as db


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=db.naming_convention)
