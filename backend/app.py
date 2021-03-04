from flask import Flask
from flask import request
from flask_cors import CORS
from parser import Parser
from comparer import Comparer
from analyzer import ResumeAnalyzer
from pdfminer import high_level
import json

p = Parser()
c = Comparer(p)
a = ResumeAnalyzer(p)

jobs = {
    "job1": "This job requires exquisite employees with React, Nodejs, angular and epic unity skills!",
    "job2": "U have to be a hot girl and have some mysql, db2, kubernetes skills bruv"
}

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

    results = {}
    for j in jobs.keys():
        c.addResumeJobDesc(txt, jobs[j])
        results[j] = str(c.compareResumeToJob())

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
    print(res)
    return json.dumps(res)

if __name__ == "__main__":
    app.run()