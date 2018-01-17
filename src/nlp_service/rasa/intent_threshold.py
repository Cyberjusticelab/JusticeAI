class IntentThreshold:
    def __init__(self, min_percent_difference=0, min_confidence_threshold=0):
        self.min_percent_difference = min_percent_difference
        self.min_confidence_threshold = min_confidence_threshold

    """
    Method which verifies the accuracy of the classification with a percentage difference between the intent with the largest confidence and the intent with the 2nd largest confidence
    classify_dict: the dict holding the intents, classification %, entities
    :returns False if percentage difference is below minimum_percent_difference
    """

    def is_sufficient(self, classify_dict):
        if len(classify_dict['intent_ranking']) > 1:
            percent_difference = self.__intent_percent_difference(classify_dict)
            highest_intent_confidence = classify_dict['intent']['confidence']
            if highest_intent_confidence < self.min_confidence_threshold or percent_difference < self.min_percent_difference:
                return False
        return True

    """
        Method used to calculate the math for the percentage difference
        intent_dict: dict holding the intents there for extraction in the method
        :returns percentage difference between top and 2nd intent
    """

    def __intent_percent_difference(self, intent_dict):
        intent_ranking = intent_dict['intent_ranking']
        confidence_top = intent_ranking[0]['confidence']
        confidence_contender = intent_ranking[1]['confidence']
        percent_difference = abs(confidence_contender - confidence_top) / (
            0.5 * (confidence_contender + confidence_top))

        return percent_difference
