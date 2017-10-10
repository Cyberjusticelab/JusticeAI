from flask import Flask, request
from controllers import chatController

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World! From the Web Backend Microservice!"


@app.route("/newclaim", methods=['POST'])
def init_claim():
    if request.method == 'POST':
        init_request = request.get_json()
        return chatController.init_claim(init_request['name'])


@app.route("/chat", methods=['POST'])
def chat():
    if request.method == 'POST':
        chat_request = request.get_json()
        return chatController.chat_message(chat_request['claim_id'], chat_request['message'])