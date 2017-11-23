from feature_extraction import feature_extraction
import init
from util.log import Log

# add command line stuff...
Log.write("Starting machine learning pipeline")
feature_extraction.run()
