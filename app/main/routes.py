from app.main import bp
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('login.html', title='Enter Name', form=form)

