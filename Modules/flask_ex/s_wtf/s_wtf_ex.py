
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField

from flask import Flask, render_template, redirect, url_for, flash


class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    remember_me = BooleanField(label='Keep me logged in')
    submit = SubmitField('Sign in')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'xc1234'


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign in', form=form)


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            'Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data
            )
        )
        return redirect(url_for('index'))
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
