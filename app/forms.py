from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, FormField, FieldList, HiddenField
from wtforms.validators import DataRequired, Email, Length


class RegistrationForm(FlaskForm):
    username = StringField('Name (First and Last)', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=128)])
    submit = SubmitField('Next')

class QuestionForm(FlaskForm):
    question_number = HiddenField()
    question_text = StringField()
    options = RadioField()
    correct_option = HiddenField()

class QuizForm(FlaskForm):
    questions = FieldList(FormField(QuestionForm), label='')
    score = HiddenField()

class QuizCategoryForm(FlaskForm):
    categories = RadioField(choices=[(1, "OTT"), (2, "DAI"), (3, "Encoding")], validators=[DataRequired()])
    submit = SubmitField('Start Quiz!')