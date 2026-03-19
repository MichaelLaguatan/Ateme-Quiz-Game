from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    def __repr__(self):
        return 'User {}'.format(self.username)
    
class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')
    def __repr__(self):
        return 'Post {}'.format(self.body)

class Questions(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    question: so.Mapped[str] = so.mapped_column(sa.String(128))
    option1: so.Mapped[str] = so.mapped_column(sa.String(128))
    option2: so.Mapped[str] = so.mapped_column(sa.String(128))
    option3: so.Mapped[str] = so.mapped_column(sa.String(128))
    option4: so.Mapped[str] = so.mapped_column(sa.String(128))
    correct_option: so.Mapped[int] = so.mapped_column(sa.Integer)

    def __repr__(self):
        return 'Questions {}'.format(self.question)