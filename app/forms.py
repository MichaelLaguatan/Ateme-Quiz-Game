from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, FormField, FieldList, HiddenField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    username=StringField('Username (First and Last)', validators=[DataRequired()])
    submit = SubmitField('Submit')

class QuestionForm(FlaskForm):
    question_number = HiddenField()
    question_text = StringField()
    options = RadioField()

class QuizForm(FlaskForm):
    questions = FieldList(FormField(QuestionForm), label='')