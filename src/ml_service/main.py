from feature_extraction import feature_extraction
from model_learning import model_training
import init
from util.log import Log

Log.write("Starting machine learning pipeline")
feature_extraction.run()
model_training.run()
