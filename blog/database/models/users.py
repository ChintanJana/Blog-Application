from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from blog.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.posts import Post

class User(Base):
    __tablename__ = 'users'

    user_id : Mapped[int] = mapped_column(primary_key=True, index=True)
    username : Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    posts : Mapped[List["Post"]] = relationship(back_populates="user", cascade="all, delete")

    def __repr__(self) -> str:
        return f"User(User Id : {self.user_id!r}, Username : {self.username!r})"