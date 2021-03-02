from flask import Flask
from flask import request
from flask_cors import CORS

import pdfplumber


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
    print(file)
    with pdfplumber.open(file) as pdf:
        print("hello")
        for page in pdf.pages:
            print(page.extract_text())
    return {"success":"file submitted"}

