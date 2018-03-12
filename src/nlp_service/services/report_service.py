from nlp_service.services import ml_service, fact_service


def generate_report(conversation, ml_prediction, similar_precedents):
    report = {}
    ml_statistics = ml_service.get_statistics()
    conversation_facts = fact_service.get_resolved_fact_keys(conversation)

    # Prediction accuracy
    report['accuracy'] = 0

    # Data set size
    report['data_set'] = ml_statistics['data_set']['size']

    # Similar case count
    report['similar_case'] = len(similar_precedents)

    # Curves
    report['curves'] = {}

    possible_curve_facts = ml_statistics['regressor']
    for fact in conversation_facts:
        if fact in possible_curve_facts:
            report['curves'][fact] = possible_curve_facts[fact]

    # Outcomes
    report['outcomes'] = dict(ml_prediction)

    # Similar Precedents
    report['similar_precedents'] = []

    # Filter out all facts and outcomes that don't matter from precedents
    for precedent in similar_precedents:
        filtered_fact_dict = {k: v for k, v in precedent['facts'].items() if k in conversation_facts}
        precedent['facts'] = filtered_fact_dict
        filtered_outcome_dict = {k: v for k, v in precedent['outcomes'].items() if k in ml_prediction}
        precedent['outcomes'] = filtered_outcome_dict
        report['similar_precedents'].append(precedent)

    return report
