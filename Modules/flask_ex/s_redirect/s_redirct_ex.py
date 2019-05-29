
from flask import Flask, redirect, url_for, render_template, request, abort

# HTTP_300_MULTIPLE_CHOICES
# HTTP_301_MOVED_PERMANENTLY
# HTTP_302_FOUND
# HTTP_303_SEE_OTHER
# HTTP_304_NOT_MODIFIED
# HTTP_305_USE_PROXY
# HTTP_306_RESERVED
# HTTP_307_TEMPORARY_REDIRECT

# 400 - 用于错误请求
# 401 - 用于未身份验证的
# 403 - Forbidden
# 404 - 未不到
# 406 - 表示不接受
# 415 - 用于不支持的媒体类型
# 429 - 请求过多

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/success')
def success():
    return 'logged in successfully'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin':
            return redirect(url_for('success'))
        else:
            abort(401)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
