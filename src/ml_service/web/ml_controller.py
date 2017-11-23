from util.file import Load
from feature_extraction.post_processing.regex.regex_fact import TagPrecedents
from flask import abort
from model_learning.svm import LinearSVM
import numpy as np

linear_classifier = LinearSVM()
linear_classifier.load()
indices = TagPrecedents().get_intent_indice()


def predict_outcome(input_json):
    demands_vector = __dict_to_vector(input_json['demands'], 'demands_vector')
    facts_vector = __dict_to_vector(input_json['facts'], 'facts_vector')
    outcome_vector = linear_classifier.predict(facts_vector)
    return __vector_to_dict(outcome_vector)


def __dict_to_vector(input_dict, input_type):
    output_vector = np.zeros(len(indices[input_type]))
    for index, val in indices[input_type]:
        if not val in input_dict:
            abort("{} is not a valid key".format(val), 400)
        output_vector[index] = int(input_dict[val])
    return output_vector


def __vector_to_dict(output_vector):
    return {"lease_resiliation": output_vector.item(0)}
