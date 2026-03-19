from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User


class RegistrationForm(FlaskForm):
    username=StringField('Username (First and Last)', validators=[DataRequired()])
    submit = SubmitField('Submit')
