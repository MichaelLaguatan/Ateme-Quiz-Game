from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import data_required

class LoginForm(FlaskForm):
    player_name = StringField('Name', validators=[data_required()])
    submit = SubmitField('Submit')

    