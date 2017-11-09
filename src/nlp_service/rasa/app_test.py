
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter


##This is the RASA Trainer
training_data = load_data('data/Problem_identifier.json')
trainer = Trainer(RasaNLUConfig("config/config_spacy.json"))
trainer.train(training_data)
model_directory = trainer.persist('./projects/default/')  # Returns the directory the model is stored in
interpreter = Interpreter.load(model_directory, RasaNLUConfig("config/config_spacy.json"))     # to use the builder, pass it as an arg when loading the model

#This is what will be outputted from the model.py file
print(interpreter.parse(u"My landlord is increasing the rent."))