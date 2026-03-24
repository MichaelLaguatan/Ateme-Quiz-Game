from app.main import bp
from flask import render_template, request, redirect, url_for
from app.forms import RegistrationForm, QuizForm, QuizCategoryForm
from app.models import User, Questions
from app import db
import csv
import sqlalchemy as sa

@bp.route('/', methods=["GET", "POST"])
@bp.route('/index', methods=["GET", "POST"])
def index():
  form = RegistrationForm()
  if form.validate_on_submit():
      user = User(username=form.username.data, score=0, time_taken=0)
      db.session.add(user)
      db.session.commit()
      return redirect(url_for('main.quiz_type', username=user.username))
  return render_template('index.html', title='Enter Name', form=form)

@bp.route('/quiz_type/<username>', methods=["GET", "POST"])
def quiz_type(username):
   form = QuizCategoryForm()
   if form.validate_on_submit():
      return redirect(url_for('main.quiz', quiz_type=form.categories.data, username=username))
   return render_template('quiz_type.html', title='Quiz Category', form=form, username=username)

@bp.route('/quiz/<username>/<quiz_type>')
def quiz(username, quiz_type):
  form = QuizForm()
  match quiz_type:
    case 1:
      db_questions = db.session.scalars(sa.select(Questions).where(Questions.category == 1)).all()
    case 2:
      db_questions = db.session.scalars(sa.select(Questions).where(Questions.category == 2)).all()
    case 3:
      db_questions = db.session.scalars(sa.select(Questions).where(Questions.category == 3)).all()
  quiz_data = [{"question": question, "choices": [("a", question.option1), ("b", question.option2), ("c", question.option3), ("d", question.option4)]} for question in db_questions]
  for q in quiz_data:
    form.questions.append_entry()
  for i, q in enumerate(quiz_data):
    question_form = form.questions[i].form
    question_form.question_number.data = i
    question_form.question_text.label = q["question"]
    question_form.options.choices = q["choices"]
  return render_template('quiz.html', title='Questions', form=form, username=username)

@bp.route('/results/<username>', methods=["GET", "POST"])
def results(username):
  user = db.session.scalar(sa.select(User).where(User.username == username))
  db_questions = db.session.scalars(sa.select(Questions)).all()
  correct = 0
  results = []
  for key, value in request.form.items():
    if key.endswith("-question_number") or key == "time_taken":
       continue
    results.append(value)
  for index, value in enumerate(results):
     if value == db_questions[int(index)].correct_option:
        correct += 1
  user.score = correct
  user.time_taken = request.form.get("time_taken")
  db.session.add(user)
  db.session.commit()
  return render_template('results.html', title='Results', correct=correct, num_questions=len(db_questions), time_taken=user.time_taken)

@bp.route('/leaderboard')
def leaderboard():
   #users = db.session.scalars(sa.select(User)).all()

   users = User.query.order_by(User.score.desc(), User.time_taken.asc()).all()
   return render_template('leaderboard.html', title='Leaderboard', users=users)

@bp.route('/read_csv')
def read_csv():
    questions = []
    db.session.query(Questions).delete()
    files = ["sample_questions_1.csv", "sample_questions_2.csv", "sample_questions_3.csv"]
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