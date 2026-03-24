import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    score: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    time_taken: so.Mapped[float] = so.mapped_column(sa.Float, index=True)
    quiz_type: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    day_taken: so.Mapped[datetime] = so.mapped_column(sa.DateTime, index=True)

    def __repr__(self):
        return 'User {}'.format(self.username)

class Questions(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    question: so.Mapped[str] = so.mapped_column(sa.String(128))
    option1: so.Mapped[str] = so.mapped_column(sa.String(128))
    option2: so.Mapped[str] = so.mapped_column(sa.String(128))
    option3: so.Mapped[str] = so.mapped_column(sa.String(128))
    option4: so.Mapped[str] = so.mapped_column(sa.String(128))
    correct_option: so.Mapped[int] = so.mapped_column(sa.Integer)
    category: so.Mapped[int] = so.mapped_column(sa.Integer)

    def __repr__(self):
        return 'Questions {}'.format(self.question)