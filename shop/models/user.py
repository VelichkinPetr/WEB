import enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean,Enum
from sqlalchemy.orm import mapped_column, relationship, Mapped
 
from models.base import Base, TimeStampMixin, IDMixin

if TYPE_CHECKING:
    from . import Profile


class UserStatus(enum.Enum):
    admin = 'admin'
    moderator = 'moderator'

class User(Base, IDMixin, TimeStampMixin):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), nullable=False, default= UserStatus.moderator)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

    profile: Mapped['Profile'] = relationship(back_populates="user")

    def __repr__(self):
        return f'id:{self.id}, email:{self.email}, status:{self.status}, profile:{[self.profile]}'