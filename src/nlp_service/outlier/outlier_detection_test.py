from outlier.outlier_detection import OutlierDetection
import os

def test_default_arguments():
    outlier_detector = OutlierDetection()
    assert os.path.isdir(outlier_detector.RASA_FACT_DIR)
    assert isinstance(outlier_detector.TFIFD_PICKLE_FILE, str)
    assert isinstance(outlier_detector.OUTLIER_PICKLE_FILE, str)
    assert outlier_detector.TFIFD_VECTORIZER is None
    assert outlier_detector.OUTLIER_ESTIMATOR is None
    assert isinstance(outlier_detector.CONTAMINATION, float)
    assert isinstance(outlier_detector.NGRAM_RANGE, tuple)

def test_initialize_fact_model():
    outlier_detector = OutlierDetection()
    outlier_detector.initialize_fact_model()
    assert os.path.isfile(outlier_detector.TFIFD_PICKLE_FILE)
    assert os.stat(outlier_detector.TFIFD_PICKLE_FILE).st_size > 0
    assert os.path.isfile(outlier_detector.OUTLIER_PICKLE_FILE)
    assert os.stat(outlier_detector.OUTLIER_PICKLE_FILE).st_size > 0

def test_predict_if_outlier_positive():
    outlier_detector = OutlierDetection()
    outlier_detector.initialize_fact_model()
    result = outlier_detector.predict_if_outlier(['iuwerw8734234234 uywier68732468234'])
    assert result[0] == -1

def test_predict_if_outlier_positive():
    outlier_detector = OutlierDetection()
    outlier_detector.initialize_fact_model()
    result = outlier_detector.predict_if_outlier(['it says on my lease that it ends on the 2nd of this month'])
    assert result[0] == 1



