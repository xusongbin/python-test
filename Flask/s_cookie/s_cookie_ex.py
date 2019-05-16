
from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/setcookie', methods=['POST', 'GET'])
def set_cookie():
    if request.method == 'POST':
        user = request.form['nm']

        resp = make_response('set_cookie')
        resp.set_cookie('userID', user)

        return resp


@app.route('/getcookie')
def get_cookie():
    name = request.cookies['userID']
    resp = make_response('get_cookie %s' % name)
    return resp


@app.route('/delcookie')
def del_cookie():
    resp = make_response('delete_cookie')
    resp.delete_cookie('userID')
    return resp


if __name__ == '__main__':
    app.run(debug=True)
