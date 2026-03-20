from app.main import bp
from flask import render_template, flash, redirect, url_for, request
from app.forms import RegistrationForm, QuizForm
from app.models import User, Questions
from app import db
import csv
import sqlalchemy as sa
import logging

@bp.route('/', methods=["GET", "POST"])
@bp.route('/index', methods=["GET", "POST"])
def index():
    form = QuizForm()
    db_questions = db.session.scalars(sa.select(Questions)).all()
    if form.is_submitted():
      correct = 0
      for question_form in form.questions:
        selected_answer = question_form.options.data
        if selected_answer == db_questions[int(question_form.question_number.data)].correct_option:
          correct += 1
      return redirect(url_for('main.results', correct=correct, num_questions=len(db_questions)))
    quiz_data = [{"question": question, "choices": [("a", question.option1), ("b", question.option2), ("c", question.option3), ("d", question.option4)]} for question in db_questions]
    for q in quiz_data:
      form.questions.append_entry()
    for i, q in enumerate(quiz_data):
      question_form = form.questions[i].form
      question_form.question_number.data = i
      question_form.question_text.label = q["question"]
      question_form.options.choices = q["choices"]
    return render_template('index.html', title='Questions', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('register.html', title='Enter Name', form=form)

@bp.route('/results/<correct>/<num_questions>')
def results(correct, num_questions):
  return render_template('results.html', title='Results', correct=correct, num_questions=num_questions)

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