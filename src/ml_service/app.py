from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
        return "Hello World! From the Machine Learning Microservice"
