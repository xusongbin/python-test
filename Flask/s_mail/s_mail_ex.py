from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = 'ak3336105@163.com'
app.config['MAIL_PASSWORD'] = '52023921033'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


@app.route("/")
def index():
    msg = Message('Hello', sender='ak3336105@163.com', recipients=['ak3336105@163.com'])
    # msg.body = 'Hello Flask message sent'
    msg.html = 'Hello Flask message sent from <b>Flask-Mail</b> stranger'
    # with app.open_resource('1.txt') as fp:
    #     msg.attach("1.txt", "text/txt", fp.read())
    mail.send(msg)
    return '<h1>邮件发送成功</h1>'


if __name__ == '__main__':
    app.run(debug=True)
