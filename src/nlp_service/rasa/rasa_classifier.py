import os

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Trainer, Interpreter


class RasaClassifier(object):
    problem_category_interpreters = {}
    fact_interpreters = {}

    def __init__(self):
        self.rasa_config = RasaNLUConfig("rasa/config/config_spacy.json")
        self.trainer = Trainer(self.rasa_config)

    def train(self):
        # Train fact classifiers
        self.__train_interpreter('rasa/data/fact/', self.fact_interpreters)

        # Train problem category classifiers
        self.__train_interpreter('rasa/data/category/', self.problem_category_interpreters)

    def classify_problem_category(self, message):
        return self.problem_category_interpreters['claim_category'].parse(message)

    def classify_fact(self, fact_name, message):
        return self.fact_interpreters[fact_name].parse(message)

    def __train_interpreter(self, training_data_dir, interpreter_dict):
        for filename in os.listdir(training_data_dir):
            fact_key = os.path.splitext(filename)[0]

            training_data = load_data(training_data_dir + filename)
            self.trainer.train(training_data)
            model_directory = self.trainer.persist(path='rasa/projects/justiceai/', fixed_model_name=fact_key)

            interpreter_dict[fact_key] = Interpreter.load(model_directory, RasaNLUConfig)
