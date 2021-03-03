from flask import Flask
from flask import request
from flask_cors import CORS

from pdfminer import high_level

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello_world():
    return "hey"


@app.route('/api/upload', methods=['POST'])
def upload():
    print(request.files)
    if 'file' not in request.files:
        return {"error":'no file submitted'}
    file = request.files['file']
    txt = high_level.extract_text(file)

    # pass text to grader here
    print(txt)

    return {"success":"file submitted"}

