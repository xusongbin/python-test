
from flask import Flask

app = Flask(__name__)


@app.route('/str/<name>')
def get_string(name):
    return 'get string %s' % name


@app.route('/int/<int:data>')
def get_int(data):
    return 'get int %d' % data


@app.route('/float/<float:data>')
def get_float(data):
    return 'get float %f' % data


if __name__ == '__main__':
    app.run()
