from flask import Flask
from flask import request
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
from controllers import nlpController

app = Flask(__name__)

##This is the RASA Trainer
training_data = load_data('rasa/data/has_lease_expired.json')  # Where to fish the data it is being trained
trainer = Trainer(RasaNLUConfig(
    "rasa/config/config_spacy.json"))  # Choosing the trainer (in this case spacy, not the default one from rasa)
trainer.train(training_data)  # Train the actual data
model_directory = trainer.persist('./projects/default/')  # Where the models are stored
interpreter = Interpreter.load(model_directory, RasaNLUConfig(
    "rasa/config/config_spacy.json"))  # to use the builder, pass it as an arg when loading the model

##interpreter will parse incoming text to the nlp_service and furnish it back in a Json Format:
'''
{'intent': 
{'name': 'greet', 
'confidence': 0.67869660247875474}, 
'entities': [], 
'intent_ranking': 
    [{'name': 'greet', 'confidence': 0.67869660247875474}, 
    {'name': 'goodbye', 'confidence': 0.14246669235938911}, 
    {'name': 'restaurant_search', 'confidence': 0.094058190578983264}, 
    {'name': 'affirm', 'confidence': 0.084778514582872916}], 
'text': 'hello'}
'''


## Results from a simple text interpreter.parse(u"hello")
@app.route("/claim_category", methods=['POST'])
def classify_claim_category():
    input = request.get_json()
    return nlpController.process_user_input(input['conversation_id'], input['message'])


@app.route("/submit_message", methods=['POST'])
def submit_message():
    input = request.get_json()
    return nlpController.process_user_input(input['conversation_id'], input['message'])
