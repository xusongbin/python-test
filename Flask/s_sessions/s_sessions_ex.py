
from flask import Flask, request, redirect, url_for


app = Flask(__name__)
app.secret_key = 'any random string'

session = {}
session['username'] = 'admin'


@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return "Logged in as %s <br><b><a href='/logout'>click here to log out</a></b>" % username
    return "You are not logged in <br><b><a href='/login'>click here to log in</a></b>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return "<form action='' method='post'><p><input type=text name=username></p><p><input type=submit value=Login></p></form>"


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
