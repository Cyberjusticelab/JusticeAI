from flask import Flask
from flask import request
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
from controllers import nlpController

app = Flask(__name__)

##This is the RASA Trainer
training_data = load_data('data/examples/rasa/demo-rasa.json') # Where to fish the data it is being trained
trainer = Trainer(RasaNLUConfig("config/config_spacy.json")) # Choosing the trainer (in this case spacy, not the default one from rasa)
trainer.train(training_data) # Train the actual data
model_directory = trainer.persist('./projects/default/')  # Where the models are stored
interpreter = Interpreter.load(model_directory, RasaNLUConfig("config/config_spacy.json"))     # to use the builder, pass it as an arg when loading the model

##interpreter now holds Json object filled with intents returning a confidence ratio

@app.route("/submit_answer", methods=['POST'])
def submit_answer():
    input = request.get_json()
    return nlpController.process_user_input(input['conversation_id'], input['message'])
