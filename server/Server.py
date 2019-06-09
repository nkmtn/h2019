from flask import Flask,request,jsonify
from flask_cors import CORS
import json
import string
import random
import time

app = Flask(__name__)
CORS(app)

def genRandomString():
    return ''.join([ random.choice(string.ascii_letters + string.digits) for i in range(32)])

TOKENS = {}

@app.route("/api/auth/login",methods = ["POST"])
def login():
    global TOKENS
    print(request.json)
    token  = genRandomString()
    TOKENS = {token:{"time":int(time.time()),"accountType":"user"}}
    print(TOKENS)
    return jsonify({"status":"success","token":token})



if __name__ == '__main__':
    app.run(host = "127.0.0.1",port=5000)