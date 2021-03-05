from flask import Flask
from flask import request
from flask_cors import CORS
from parserFnc import Parser
from comparer import Comparer
from analyzer import ResumeAnalyzer
from pdfminer import high_level
from dotenv import load_dotenv
import json
import psycopg2
import os
import sys
import signal


load_dotenv()
p = Parser()
c = Comparer(p, 30000)
a = ResumeAnalyzer(p)
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
    file = request.files.get('file', None)
    txt = high_level.extract_text(file)
    
    print(txt)
    try:
        conn = psycopg2.connect("{}".format(os.getenv("URI"))) 
        cur = conn.cursor()

        cur.execute("Select * FROM jobs LIMIT 0")
        colnames = [desc[0] for desc in cur.description]

        cur.execute("SELECT * FROM jobs;")
        results = []
        c.addResume(txt)

        for row in cur:
            indRes = {}
            for i, colName in enumerate(colnames):
                indRes[colName] = row[i]
            c.addJobDesc(row[1])
            indRes['grade'] = (c.compareResumeToJob())
            results.append(indRes)
        conn.close()
        return {"data": results}
    except Exception as e:
        print("Error occured, closing connection.")
        print(e)
        conn.close()
        return "Error occured"
    return results
    

"""
Format: {"resume": "..."}
"""
@app.route('/api/testParser', methods=['POST'])
def testParser():
    try :
        conn = psycopg2.connect("{}".format(os.getenv("URI"))) 
        cur = conn.cursor()

        cur.execute("Select * FROM jobs LIMIT 0")
        colnames = [desc[0] for desc in cur.description]
        
        cur.execute("SELECT * FROM jobs;")

        reqJSON = request.json
        results = []
        c.addResume(reqJSON['resume'])
        for row in cur:
            indRes = {}
            for i, colName in enumerate(colnames):
                indRes[colName] = row[i]
            c.addJobDesc(row[1])
            indRes['grade'] = (c.compareResumeToJob())
            results.append(indRes)
        conn.close()
        return {"data": results}
    except Exception as e:
        print("Error occured, closing connection.")
        print(e)
        conn.close()
        return "Error occured"

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