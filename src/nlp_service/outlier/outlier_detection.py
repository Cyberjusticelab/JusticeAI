import glob
import os
import json
import pickle


class OutlierDetection:
    def __init__(self):
        self.RASA_FACT_DIR = os.getcwd() + '/rasa/data/fact/'
        self.TFIFD_PICKLE_FILE = os.getcwd() + '/outlier/tfidf_vectorizer'
        self.OUTLIER_PICKLE_FILE = os.getcwd() + '/outlier/outlier_estimator'
        self.TFIFD_VECTORIZER = None
        self.OUTLIER_ESTIMATOR = None

        # The proportion of the data set that is considered as an outlier
        self.CONTAMINATION = 0.2
        self.NGRAM_RANGE = (1, 2)

    def initialize_fact_model(self):
        # Extract all RASA training sentences for all facts
        rasa_fact_paths = glob.glob(self.RASA_FACT_DIR + '*.json')
        all_sentences = []
        for fact_path in rasa_fact_paths:
            with open(fact_path, 'r') as f:
                file_json = json.loads(f.read().encode('utf-8'))
            for example in file_json['rasa_nlu_data']['common_examples']:
                all_sentences.append(example['text'].lower())


        # TF-IDF model
        from sklearn.feature_extraction.text import TfidfVectorizer
        tfidf_vectorizer = TfidfVectorizer(ngram_range=self.NGRAM_RANGE, strip_accents='ascii')
        X_tfidf = tfidf_vectorizer.fit_transform(all_sentences)

        # Fit to robust covariance estimation
        from sklearn.covariance import EllipticEnvelope
        outlier_estimator = EllipticEnvelope(contamination=self.CONTAMINATION)
        outlier_estimator.fit(X_tfidf.toarray())

        # Binarize for future use
        with open(self.TFIFD_PICKLE_FILE, 'wb') as f:
            pickle.dump(tfidf_vectorizer, f)
        with open(self.OUTLIER_PICKLE_FILE, 'wb') as f:
            pickle.dump(outlier_estimator, f)


    def predict_if_outlier(self, sentences):
        self._ensure_unpickled_models()

        # Predit whether new sentences are outliers
        results = self.TFIFD_VECTORIZER.transform(sentences)
        return self.OUTLIER_ESTIMATOR.predict(results.toarray())

    def _ensure_unpickled_models(self):
        if not self.TFIFD_VECTORIZER:
            with open(self.TFIFD_PICKLE_FILE, 'rb') as f:
                self.TFIFD_VECTORIZER = pickle.load(f)
        if not self.OUTLIER_ESTIMATOR:
            with open(self.OUTLIER_PICKLE_FILE, 'rb') as f:
                self.OUTLIER_ESTIMATOR = pickle.load(f)


