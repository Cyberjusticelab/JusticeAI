from feature_extraction.post_processing.regex.regex_tagger import TagPrecedents
from model_training.classifier.multi_class_svm import MultiClassSVM
from model_training.regression.multi_class_svr import MultiClassSVR
import numpy as np


class MlController:
    indexes = TagPrecedents().get_intent_index()
    classifier_model = MultiClassSVM()
    regression_model = MultiClassSVR()
    classifier_labels = classifier_model.load_classifier_labels()

    @staticmethod
    def predict_outcome(input_json):
        """
        Makes a prediction based on the input json
        input_json: Dict containing the facts and demands
        The input json must be as follows:
            {
                "facts" : {
                    "fact1": 1 or 0,
                    "fact2": 1 or 0,
                    "fact3": 1 or 0,
                    etc
                }
            }

        It is not necessary to include ALL demands or facts,
        some may be omitted
        returns: a dict containing all the predictions
                 currently, its format is as follows:
                 {
                     "lease_resiliation" : 1 or 0
                 }
        """

        int_facts_vector = MlController.dict_to_vector(input_json['facts'])
        integer_outcome_vector = MlController.regression_model.predict(int_facts_vector)[0]

        bool_facts_vector = MlController.dict_to_vector(input_json['facts'])
        binary_outcome_vector = MlController.classifier_model.predict(bool_facts_vector)[0]

        return MlController.vector_to_dict(binary_outcome_vector, integer_outcome_vector)

    @staticmethod
    def dict_to_vector(input_dict):
        """
        Converts a dictionary to vector form, readable by ML
        input_dict: dictionary containing all facts or demands
                    It is as follows:
                    {
                        "fact 1": <int>,
                        "fact 2": <int>,
                        "fact 3": <int>,
                        ...
                    }
        returns: a vector integers
        """
        output_vector = np.zeros(len(MlController.indexes['facts_vector']))
        for index, val in MlController.indexes['facts_vector']:
            if val in input_dict:
                output_vector[index] = int(input_dict[val])
        return output_vector

    @staticmethod
    def vector_to_dict(binary_outcome_vector, integer_outcome_vector):
        return_dict = {}
        for outcome_index in MlController.classifier_labels:
            label = MlController.classifier_labels[outcome_index]
            return_dict[label] = str(binary_outcome_vector[outcome_index])

        for outcome_tuples in MlController.indexes['outcomes_vector']:
            outcome_index = outcome_tuples[0]
            label = outcome_tuples[1]
            if label not in return_dict:
                value = int(integer_outcome_vector[outcome_index])
                # need asymptote I think in regression training
                if value < 0:
                    value = 0
                return_dict[label] = str(value)

        return {'outcomes_vector': return_dict}
