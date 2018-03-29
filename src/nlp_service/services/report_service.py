import statistics

from nlp_service.services import ml_service, fact_service


def generate_report(conversation, ml_prediction, similar_precedents, probabilities_dict):
    """
    Generates a report for a prediction based on ML input
    :param conversation: The current Conversation
    :param ml_prediction: A dictionary of outcomes for the conversation received from ml_service
    :param similar_precedents: A list of dicts containing precedents similar to the current case
    :param probabilities_dict: A dict of probabilities for every outcome classifier
    :return: A dict of a report detailing the prediction made by the ml_service
    """

    report = {}
    ml_statistics = ml_service.get_statistics()
    conversation_facts = fact_service.get_resolved_fact_keys(conversation)

    # Prediction accuracy
    report['accuracy'] = 0

    relevant_probabilities_dict = {k: v for k, v in probabilities_dict.items() if k in ml_prediction}
    accuracy_mean = statistics.mean([float(v) for k, v in relevant_probabilities_dict.items()])
    report['accuracy'] = accuracy_mean

    # Data set size
    report['data_set'] = ml_statistics['data_set']['size']

    # Similar case count
    report['similar_case'] = len(similar_precedents)

    # Curves
    report['curves'] = {}

    possible_curve_outcomes = ml_statistics['regressor']
    for outcome in ml_prediction:
        if outcome in possible_curve_outcomes:
            report['curves'][outcome] = dict(possible_curve_outcomes[outcome])
            report['curves'][outcome]['outcome_value'] = ml_prediction[outcome]

    # Outcomes
    report['outcomes'] = {}

    for outcome in ml_prediction:
        if int(ml_prediction[outcome]) == 1:
            report['outcomes'][outcome] = True
        elif int(ml_prediction[outcome]) == 0:
            report['outcomes'][outcome] = False
        else:
            report['outcomes'][outcome] = ml_prediction[outcome]

    # Similar Precedents
    report['similar_precedents'] = []

    # Filter out all facts and outcomes that don't matter from precedents
    for precedent in similar_precedents:
        filtered_fact_dict = {k: v for k, v in precedent['facts'].items() if k in conversation_facts}
        precedent['facts'] = __dict_values_to_int(filtered_fact_dict)
        filtered_outcome_dict = {k: v for k, v in precedent['outcomes'].items() if k in ml_prediction}
        precedent['outcomes'] = __dict_values_to_int(filtered_outcome_dict)
        report['similar_precedents'].append(precedent)

    return report


def __dict_values_to_int(dict):
    for key in dict:
        if isinstance(dict[key], str):
            try:
                dict[key] = int(float(dict[key]))
            except ValueError:
                pass
    return dict
