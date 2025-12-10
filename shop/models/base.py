from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from datetime import datetime
from sqlalchemy import DateTime, func, Integer, Table, Column, ForeignKey


class Base(DeclarativeBase):
    pass


class IDMixin:
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index= True
    )

class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= func.now(),
        server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= func.now(),
        server_default=func.now(),
        onupdate=func.now()
    )

products_categories = Table(
    "products_categories",
        Base.metadata,
        Column("products", ForeignKey("products.id"), primary_key=True),
        Column("categories", ForeignKey("categories.id"), primary_key=True),
    )