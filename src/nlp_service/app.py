from flask import Flask
from flask import request
from rasa.converters import load_data
from rasa.config import RasaNLUConfig
from rasa.model import Trainer
from rasa.model import Metadata, Interpreter
from controllers import nlpController

app = Flask(__name__)

##This is the RASA Trainer
training_data = load_data('data/data.json') # Where to fish the data it is being trained
trainer = Trainer(RasaNLUConfig("config/config_spacy.json")) # Choosing the trainer (in this case spacy, not the default one from rasa)
trainer.train(training_data) # Train the actual data
model_directory = trainer.persist('./projects/default/')  # Where the models are stored
interpreter = Interpreter.load(model_directory, RasaNLUConfig("config/config_spacy.json"))     # to use the builder, pass it as an arg when loading the model

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

@app.route("/submit_answer", methods=['POST'])
def submit_answer():
    input = request.get_json()
    return nlpController.process_user_input(input['conversation_id'], input['message'])
