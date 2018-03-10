import numpy as np

from util.file import Load
from feature_extraction.post_processing.regex.regex_tagger import TagPrecedents
from model_training.classifier.multi_output.multi_class_svm import MultiClassSVM
from model_training.regression.multi_output.multi_output_regression import MultiOutputRegression
from model_training.similar_finder.similar_finder import SimilarFinder


class MlController:
    indexes = TagPrecedents().get_intent_index()
    classifier_labels = MultiClassSVM.load_classifier_labels()
    classifier_model = MultiClassSVM()
    regression_model = MultiOutputRegression()
    similar_finder = SimilarFinder()
    precedent_vectors = Load.load_binary("precedent_vectors.bin")

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
        facts_vector = MlController.fact_dict_to_vector(input_json['facts'])
        outcome_vector = MlController.classifier_model.predict(facts_vector)[0]
        outcome_vector = MlController.regression_model.predict(facts_vector, outcome_vector)
        response = MlController.outcome_vector_to_dict(outcome_vector)
        similar_dict = {'facts_vector': facts_vector, 'outcomes_vector': outcome_vector}
        response['similar_precedents'] = MlController.format_similar_precedents(
            MlController.similar_finder.get_most_similar(similar_dict))
        return response

    @staticmethod
    def fact_dict_to_vector(input_dict):
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
    def outcome_vector_to_dict(outcome_vector):
        return_dict = {}
        for outcome_index in MlController.classifier_labels:
            label = MlController.classifier_labels[outcome_index][0]
            return_dict[label] = str(outcome_vector[outcome_index])
        return {'outcomes_vector': return_dict}

    @staticmethod
    def fact_vector_to_dict(fact_vector):
        return_dict = {}
        for fact_tuple in MlController.indexes['facts_vector']:
            label = fact_tuple[1]
            return_dict[label] = str(fact_vector[fact_tuple[0]])
        return {'facts': return_dict}

    @staticmethod
    def format_similar_precedents(similarity_list):
        """
        Formats a list such as ["AZ-111111", 1.5] into a list of dicts of the form
        [{"precedent": "AZ-111111","distance": 1.5}]
        :param similarity_list: List of lists of the form ["PRECEDENT_NAME"(string), DISTANCE(number)]
        :return: A formatted list of precedents
        """
        formatted_precedents = []

        for precedent_array in similarity_list:
            precedent = {
                "precedent": precedent_array[0].split(".")[0],
                "distance": precedent_array[1],
                "facts": MlController.fact_vector_to_dict(MlController.precedent_vectors[precedent_array[0]]['facts_vector'])['facts'],
                "outcomes": MlController.outcome_vector_to_dict(
                    MlController.precedent_vectors[precedent_array[0]]['outcomes_vector']
                )['outcomes_vector'],
            }
            for fact_tuple in MlController.indexes['facts_vector']:
                if fact_tuple[2] == 'bool':
                    precedent['facts'][fact_tuple[1]] = bool(float(precedent['facts'][fact_tuple[1]]))
            for outcome_tuple in MlController.classifier_labels.values():
                if outcome_tuple[1] == 'bool':
                    precedent['outcomes'][outcome_tuple[0]] = bool(float(precedent['outcomes'][outcome_tuple[0]]))
            formatted_precedents.append(precedent)
        return formatted_precedents

    @staticmethod
    def get_weighted_facts():
        """
        :return:
            {
            'additional_indemnity_money': {
                'important_facts': [
                    ...
                ],
                'additional_facts': [
                    ...
                ]
            }
        """
        return MlController.classifier_model.get_ordered_weights()

    @staticmethod
    def get_anti_facts():
        return {
            'tenant_individual_responsability': 'tenant_group_responsability',
            'tenant_lease_fixed': 'tenant_lease_indeterminate',
            'tenant_rent_not_paid_less_3_weeks': 'tenant_rent_not_paid_more_3_weeks',
            'not_violent': 'violent'
        }
