from app.main import bp
from flask import render_template, flash, redirect, url_for
from app.forms import RegistrationForm, QuestionForm, QuizForm
from app.models import User, Questions
from app import db
import csv
import sqlalchemy as sa
import logging

@bp.route('/')
@bp.route('/index')
def index():
    form = QuizForm()
    db_questions = db.session.scalars(sa.select(Questions)).all()
    quiz_data = [{"question": question, "choices": [("a", question.option1), ("b", question.option2), ("c", question.option3), ("d", question.option4)]} for question in db_questions]
    for q in quiz_data:
      form.questions.append_entry()
    for i, q in enumerate(quiz_data):
      question_form = form.questions[i].form
      question_form.question_text.label = q["question"]
      question_form.options.choices = q["choices"]
    return render_template('index.html', title='Questions', db_questions=db_questions, form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('register.html', title='Enter Name', form=form)


@bp.route('/read_csv')
def read_csv():
    questions = []
    db.session.query(Questions).delete()
    with open('sample_questions.csv', mode = 'r', encoding='utf-8-sig') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            question = Questions(question=lines[0], option1=lines[1], option2=lines[2], option3=lines[3], option4=lines[4], correct_option=lines[5])
            db.session.add(question)
            questions.append((lines[0], lines[1], lines[2], lines[3], lines[4], lines[5]))
    db.session.commit()
    for question in questions:
        print(question)
    return questions