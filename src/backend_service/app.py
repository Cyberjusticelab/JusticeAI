from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://justiceai:justiceai@localhost/justiceai'
db = SQLAlchemy(app)

from controllers import chatController

@app.route("/")
def hello():
    return "Hello World! From the Web Backend Microservice!"


@app.route("/new", methods=['POST'])
def init_claim():
    if request.method == 'POST':
        init_request = request.get_json()
        return chatController.init_conversation(init_request['name'])


@app.route("/chat", methods=['POST'])
def chat():
    if request.method == 'POST':
        chat_request = request.get_json()
        return chatController.chat_message(chat_request['conversation_id'], chat_request['message'])
