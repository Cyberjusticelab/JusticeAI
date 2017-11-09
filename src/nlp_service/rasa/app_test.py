import time
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
from rasa_nlu.components import ComponentBuilder


builder = ComponentBuilder(use_cache=True)
##This is the RASA Trainer
start_time = time.localtime(time.time())
training_data = load_data('data/Problem_identifier.json')
trainer = Trainer(RasaNLUConfig("config/config_spacy.json"), builder)
trainer.train(training_data)
training_time = time.localtime(time.time())
model_directory = trainer.persist('./projects/default/')  # Returns the directory the model is stored in
first_time = time.localtime(time.time())
interpreter = Interpreter.load(model_directory, RasaNLUConfig("config/config_spacy.json"), builder)     # to use the builder, pass it as an arg when loading the model
second_time = time.localtime(time.time())

second_interpreter = Interpreter.load(model_directory, RasaNLUConfig("config/config_spacy.json"), builder)

third_time = time.localtime(time.time())

#This is what will be outputted from the model.py file
print(interpreter.parse(u" I'm being evicted. "))

fourth_time = time.localtime(time.time())

print(second_interpreter.parse(u"I'm being evicted"))

fifth_time = time.localtime(time.time())

print(start_time)
print(training_time)
print(first_time)
print(second_time)
print(third_time)
print(fourth_time)
print(fifth_time)