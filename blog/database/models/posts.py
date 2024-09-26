from sqlalchemy import Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from blog.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.users import User

class Post(Base):
    __tablename__ = 'posts'

    post_id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title : Mapped[str] =  mapped_column(String(50))
    content : Mapped[str] = mapped_column(String(100))
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    published : Mapped[bool] = mapped_column(Boolean, default=True)
    user : Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(Post Id : {self.post_id!r}, User Id : {self.user_id!r})"