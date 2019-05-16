
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/score/<int:data>')
def hello_score(data):
    return render_template('score.html', marks=data)


if __name__ == '__main__':
    app.run(debug=True)
