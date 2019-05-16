
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/form')
def test_form():
    _dict = {'phy': 50, 'che': 60, 'maths': 70}
    return render_template('dict.html', result=_dict)


if __name__ == '__main__':
    app.run()
