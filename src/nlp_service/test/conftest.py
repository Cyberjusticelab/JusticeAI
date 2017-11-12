from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

import pytest
from rasa_nlu import data_router
from rasa_nlu.components import ComponentBuilder
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Interpreter
from rasa_nlu.model import Trainer

# Building paths to config files and data files
CONFIG_PATH_CONFIG = "rasa/config/config_spacy.json"
DATA_FILE_CATEGORY = "rasa/data/category/claim_category.json"
DATA_FILE_HAS_LEASE_EXPIRED = "rasa/data/fact/has_lease_expired.json"
DATA_FILE_IS_HABITABLE = "rasa/data/fact/is_habitable.json"
DATA_FILE_LEASE_TYPE = "rasa/data/fact/lease_type.json"

# This avoids deadlocks in the test suite - Rasa Doc
data_router.DEFERRED_RUN_IN_REACTOR_THREAD = False


@pytest.fixture(scope="session")
def component_builder():
    return ComponentBuilder()


@pytest.fixture(scope="session")
def spacy_nlp(default_config):
    return component_builder.create_component("nlp_spacy", default_config)


@pytest.fixture(scope="session")
def default_config():
    return RasaNLUConfig(CONFIG_PATH_CONFIG)

@pytest.fixture(scope="session")
def train_models():
    ##This is the RASA Trainer
    interpreters = {}
    trainer = Trainer(default_config)
    trainingDirectory = 'rasa/data/fact'
    for filename in os.listdir(trainingDirectory):
        fact_key = os.path.splitext(filename)[0]

        training_data = load_data(trainingDirectory + filename)
        trainer.train(training_data)
        model_directory = trainer.persist(path='.rasa/projects/justiceai', fixed_model_name=fact_key)

        interpreters[fact_key] = Interpreter.load(model_directory, RasaNLUConfig)

    return interpreters

@pytest.fixture(scope="session")
def teardown_models():
    print("Teardown of models")
    path = "rasa/projects/justiceai/default"
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
'''
Example of use
interpreters['is_student'].parse(u"I am a student.")
interpreters['is_habitable'].parse(u"It smells pretty bad but overall it's a livable place.")
interpreters['has_lease_expired'].parse(u"Yes my lease expired.")
interpreters['lease_type'].parse(u"My lease ends in June.")
'''