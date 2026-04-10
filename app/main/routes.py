from app.main import bp
from flask import render_template, request, redirect, url_for, session
from app.forms import RegistrationForm, QuizForm, QuizCategoryForm
from app.models import User, Questions
from app import db
import csv
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy import func

QUESTION_AMOUNT = 5

@bp.route('/', methods=["GET", "POST"])
@bp.route('/index', methods=["GET", "POST"])
def index():
  form = RegistrationForm()
  if form.validate_on_submit():
      session['username'] = form.username.data
      session['email'] = form.email.data
      return redirect(url_for('main.quiz_type'))
  return render_template('index.html', title='Enter Name', form=form)

@bp.route('/quiz_type', methods=["GET", "POST"])
def quiz_type():
  form = QuizCategoryForm()
  if form.validate_on_submit():
      session['quiz_type'] = form.categories.data
      return redirect(url_for('main.quiz'))
  return render_template('quiz_type.html', title='Quiz Category', form=form)

@bp.route('/quiz')
def quiz():
  form = QuizForm()
  db_questions = []
  match session['quiz_type']:
    case '1':
      db_questions = db.session.scalars(sa.select(Questions).where(Questions.category == 1).order_by(func.random()).limit(QUESTION_AMOUNT)).all()
    case '2':
      db_questions = db.session.scalars(sa.select(Questions).where(Questions.category == 2).order_by(func.random()).limit(QUESTION_AMOUNT)).all()
    case '3':
      db_questions = db.session.scalars(sa.select(Questions).where(Questions.category == 3).order_by(func.random()).limit(QUESTION_AMOUNT)).all()
  quiz_data = [{"question": question, 
              "choices": [("a", question.option1),
                          ("b", question.option2),
                          ("c", question.option3),
                          ("d", question.option4)],
              "correct_choice": question.correct_option} for question in db_questions]
  for q in quiz_data:
    form.questions.append_entry()
  for i, q in enumerate(quiz_data):
    question_form = form.questions[i].form
    question_form.question_number.data = i
    question_form.question_text.label = q["question"]
    question_form.options.choices = q["choices"]
    question_form.correct_option.data = q["correct_choice"]
  return render_template('quiz.jinja2', title='Questions', form=form)

@bp.route('/results', methods=["GET", "POST"])
def results():
  user = User(username=session['username'], email=session['email'], score=request.form.get('score'), time_taken=request.form.get('time_taken'), quiz_type=session['quiz_type'], day_taken=datetime.now())
  db.session.add(user)
  db.session.commit()
  return render_template('results.html', title='Results', correct=user.score, num_questions=QUESTION_AMOUNT, time_taken=user.time_taken)
"""
{
  "March 10": {
    "1": [
      "Sally",
      "Bob"
    ]
    "2": [
      "Emelie"
    ]
    "3": []
  },
  "March 11": {
    "1": []
    "2": []
    "3": []
  }
}

"""

@bp.route('/leaderboard')
def leaderboard():
  users = User.query.order_by(User.score.desc(), User.time_taken.asc()).all()
  users_by_day_taken = {}
  for user in users:
    if user.quiz_type == 0:
      continue
    if str(user.day_taken.day) not in users_by_day_taken:
      users_by_day_taken[str(user.day_taken.day)] = {'1': [], '2':[], '3':[]}
    if len(users_by_day_taken[str(user.day_taken.day)][str(user.quiz_type)]) == 10:
      continue
    users_by_day_taken[str(user.day_taken.day)][str(user.quiz_type)].append(user)
  sorted_users_by_day_taken = dict(sorted(users_by_day_taken.items()))
  top_users = sorted(users, key=lambda u: (-u.score, u.time_taken))[:3]
  top_users_as_dicts = [user.__dict__ for user in top_users]
  for user in top_users_as_dicts:
    user.pop('_sa_instance_state', None)
  return render_template('leaderboard.jinja2', title='Leaderboard', sorted_users_by_day_taken=sorted_users_by_day_taken, top_users=top_users_as_dicts)

@bp.route('/read_csv')
def read_csv():
    questions = []
    db.session.query(Questions).delete()
    files = ["questions_1.csv", "questions_2.csv", "questions_3.csv"]
    for index, file in enumerate(files):
      with open(file, mode = 'r', encoding='utf-8-sig') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            question = Questions(question=lines[0], option1=lines[1], option2=lines[2], option3=lines[3], option4=lines[4], correct_option=lines[5], category=index+1)
            db.session.add(question)
            questions.append((lines[0], lines[1], lines[2], lines[3], lines[4], lines[5]))
    db.session.commit()
    return questions

@bp.route('/clear_db', methods=["POST"])
def clear_db():
  db.drop_all()
  db.create_all()
  db.session.commit()
  return '', 204