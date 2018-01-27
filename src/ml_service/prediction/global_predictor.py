from model_training.classifier.multi_class_svm import MultiClassSVM


class GlobalPredictor:
    classifier_model = MultiClassSVM()
    classifier_labels = classifier_model.load_classifier_labels()
    regressor_model = None

    def __init__(self):
        pass

    @staticmethod
    def predict_outcome(data):
        outcome_vector = GlobalPredictor.classifier_model.predict(data)
        for i in range(len(outcome_vector)):
            if outcome_vector[i] == 1:
                column_name = GlobalPredictor.classifier_labels[i][0]
                if column_name == 'tenant_ordered_to_pay_landlord':
                    outcome_vector[i] = GlobalPredictor.regressor_model.predict(data)
        return outcome_vector
