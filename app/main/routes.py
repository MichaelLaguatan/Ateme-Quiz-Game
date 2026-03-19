from app.main import bp
from flask import render_template, flash, redirect, url_for
from app.forms import RegistrationForm
from app.models import User, Questions
from app import db
import csv
import sqlalchemy as sa


@bp.route('/read_csv')
def read_csv():
    with open('sample_questions.csv', mode = 'r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            question = Questions(lines[0], lines[1], lines[2], lines[3], lines[4], lines[5])
            db.session.add(question)
    db.session.commit()



@bp.route('/')
@bp.route('/index')
def index():
    db_questions = db.session.scalars(sa.select(Questions)).all()
    return render_template('index.html', title='Questions', db_questions=db_questions)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('register.html', title='Enter Name', form=form)



