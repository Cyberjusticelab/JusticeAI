import os
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Interpreter
from rasa_nlu.model import Trainer

##This is the RASA Trainer
interpreters = {}
RasaNLUConfig = RasaNLUConfig("config/config_spacy.json")
trainer = Trainer(RasaNLUConfig)

trainingDirectory = 'data/fact/'
for filename in os.listdir(trainingDirectory):
    fact_key = os.path.splitext(filename)[0]

    training_data = load_data(trainingDirectory + filename)
    trainer.train(training_data)
    model_directory = trainer.persist(path='./projects/justiceai/', fixed_model_name=fact_key)

    interpreters[fact_key] = Interpreter.load(model_directory, RasaNLUConfig)

print(interpreters['is_student'].parse(u"I am not a student."))
print(interpreters['is_habitable'].parse(u"It smells pretty bad but overall it's a livable place."))
print(interpreters['has_lease_expired'].parse(u"Yes my lease expired."))
print(interpreters['lease_type'].parse(u"My lease ends in June."))
