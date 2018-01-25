from rasa.rasa_classifier import RasaClassifier
from util.parse_dataset import CreateJson

# Generate RASA training data from text files
jsonCreator = CreateJson()
jsonCreator.parse_directory("/rasa/text/", "/rasa/data/fact/")

# Generate model data for training
rasa = RasaClassifier()
rasa.train(force_train=True, initialize_interpreters=False)
