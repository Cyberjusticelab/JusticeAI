from api import app
from flask import request, jsonify


@app.route("/")
def hello():
    return "Hello World! From the Web Backend Microservice!"


@app.route("/newchat", methods=['GET', 'POST'])
def init_session():
    if request.method == 'GET':
        data = {'id': 12345}
        return jsonify({'session': data})
