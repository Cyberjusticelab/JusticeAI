from feature_extraction.post_processing.regex.regex_tagger import TagPrecedents
from prediction.global_predictor import GlobalPredictor
import numpy as np


class MlController:
    indexes = TagPrecedents().get_intent_index()

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
        facts_vector = MlController.dict_to_vector(input_json['facts'])
        outcome_vector = GlobalPredictor.predict_outcome(facts_vector)

        return MlController.vector_to_dict(outcome_vector)

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
        for index, val, data_type in MlController.indexes['facts_vector']:
            if val in input_dict:
                output_vector[index] = int(input_dict[val])
        return output_vector

    @staticmethod
    def vector_to_dict(outcome_vector):
        return_dict = {}
        for outcome_index in GlobalPredictor.classifier_labels:
            label = GlobalPredictor.classifier_labels[outcome_index][0]
            return_dict[label] = str(outcome_vector[outcome_index])

        return {'outcomes_vector': return_dict}
 