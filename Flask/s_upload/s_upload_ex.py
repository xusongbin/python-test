
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from pypinyin import lazy_pinyin

app = Flask(__name__)


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        f = request.files['file']
        # print(f.filename)
        # f.save(secure_filename(''.join(lazy_pinyin(f.filename))))
        f.save(f.filename)
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True)
