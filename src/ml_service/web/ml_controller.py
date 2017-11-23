from util.file import Load
from feature_extraction.post_processing.regex.regex_fact import TagPrecedents
from flask import abort
from model_training.svm import LinearSVM
import numpy as np

linear_classifier = LinearSVM()
linear_classifier.load()
indices = TagPrecedents().get_intent_indice()


def predict_outcome(input_json):
    """
        Makes a prediction based on the input json
        input_json: Dict containing the facts and demands
                    The input json must be as follows:
                    {
                        "demands" : {
                            "demand1": 1 or 0,
                            "demand2": 1 or 0,
                            "demand3": 1 or 0,
                            etc
                        },
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
    demands_vector = __dict_to_vector(input_json['demands'], 'demands_vector')
    facts_vector = __dict_to_vector(input_json['facts'], 'facts_vector')
    outcome_vector = linear_classifier.predict(facts_vector)
    return __vector_to_dict(outcome_vector)


def __dict_to_vector(input_dict, input_type):
    """
        Converts a dictionary to vector form, readable by ML
        input_dict: dictionary containing all facts or demands
                    It is as follows:
                    {
                        "demand1": 1 or 0,
                        "demand2": 1 or 0,
                        "demand3": 1 or 0,
                        etc
                    }
        input_type: either 'facts_vector' or 'demands_vector', depending
                    on which is being generated
        returns: a vector of 1s and 0s
    """
    output_vector = np.zeros(len(indices[input_type]))
    for index, val in indices[input_type]:
        if not val in input_dict:
            abort("{} is not a valid key".format(val), 400)
        output_vector[index] = int(input_dict[val])
    return output_vector


def __vector_to_dict(output_vector):
    return {"lease_resiliation": output_vector.item(0)}
