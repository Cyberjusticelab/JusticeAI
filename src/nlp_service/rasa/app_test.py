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

print(interpreters['is_student'].parse(u"I am a student."))
print(interpreters['is_habitable'].parse(u"It smells pretty bad but overall it's a livable place."))
print(interpreters['has_lease_expired'].parse(u"Yes my lease expired."))
print(interpreters['lease_type'].parse(u"My lease ends in June."))

# {'intent': {'confidence': 0.65315696536207235, 'name': 'ask_lease_termination'},
#  'entities': [{'value': 'faggot', 'entity': 'person', 'start': 3, 'end': 9, 'extractor': 'ner_crf'},
#               {'value': 'landlord', 'entity': 'person', 'start': 10, 'end': 18, 'extractor': 'ner_crf'},
#               {'value': 'end', 'extractor': 'ner_crf', 'processors': ['ner_synonyms'], 'entity': 'terminate',
#                'start': 28, 'end': 33}],
#  'text': 'My faggot landlord wants to evict me because I smoke so much pot every single day',
#  'intent_ranking': [{'confidence': 0.65315696536207235, 'name': 'ask_lease_termination'},
#                     {'confidence': 0.22098501884144089, 'name': 'ask_nonpayment'},
#                     {'confidence': 0.06632963866741079, 'name': 'ask_rent_change'},
#                     {'confidence': 0.059528377129076028, 'name': 'ask_deposit'}]}
