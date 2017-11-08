from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter


##This is the RASA Trainer
training_data = load_data('data/data.json') # Where to fish the data it is being trained
trainer = Trainer(RasaNLUConfig("config/config_spacy.json")) # Choosing the trainer (in this case spacy, not the default one from rasa)
trainer.train(training_data) # Train the actual data
model_directory = trainer.persist('./projects/default/')  # Where the models are stored
interpreter = Interpreter.load(model_directory, RasaNLUConfig("config/config_spacy.json"))     # to use the builder, pass it as an arg when loading the model


#This is what will be outputted from the model.py file
print(interpreter.parse(u"hello"))