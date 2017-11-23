from rasa.rasa_classifier import RasaClassifier
from outlier.outlier_detection import OutlierDetection

# Generate model data for training
rasa = RasaClassifier()
rasa.train(force_train=True, initialize_interpreters=False)
