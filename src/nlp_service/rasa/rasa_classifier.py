from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Trainer


class RasaClassifier(object):



    def __init__(self):
        self.trainer = Trainer(RasaNLUConfig("config/config_spacy.json"))
        pass

    def train(self):
        training_data = load_data('data/is_student.json')
        self.trainer.train(training_data)
        pass

    def classify_problem_category(self, message):
        pass

    def classify_fact(self, fact_name, message):
        pass
