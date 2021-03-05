from flask import Flask
from flask import request
from flask_cors import CORS

from werkzeug.utils import secure_filename
from parserFnc import Parser
from comparer import Comparer
from analyzer import ResumeAnalyzer
from pdfminer import high_level

import json
import os

p = Parser()
c = Comparer(p)
a = ResumeAnalyzer(p)

jobs = {
    "job1": "This job requires exquisite employees with React, Nodejs, angular and epic unity skills!",
    "job2": "U have to be a hot girl and have some mysql, db2, kubernetes skills bruv"
}

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = os.path.join('.','static','pdfs')
ALLOWED_EXTENSIONS = { 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return {"error":'no file submitted'}
    file = request.files['file']
    if file.filename == '':
        return {"error":"no file selected"}
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(save_location)

    txt = high_level.extract_text(save_location)

    results = {}
    for j in jobs.keys():
        c.addResumeJobDesc(txt, jobs[j])
        results[j] = str(c.compareResumeToJob())

    os.remove(save_location)

    return results

"""
Format: {"resume": "...", "jobDescription": "..."}
"""
@app.route('/api/testParser', methods=['POST'])
def testParser():
    resJSON = request.json
    results = {}
    for j in jobs.keys():
        c.addResumeJobDesc(resJSON['resume'], jobs[j])
        results[j] = str(c.compareResumeToJob())
    return results

"""
Format: {"resume": "..."}
"""
@app.route('/api/upload/analyze', methods=['POST'])
def keywordCategory():
    resJSON = request.json
    a.addResume(resJSON['resume'])
    res = a.analyzeResume()
    return res

if __name__ == "__main__":
    app.run()