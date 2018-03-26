from model_training.classifier.multi_output.multi_class_svm import MultiClassSVM
from model_training.regression.single_output_regression.tenant_pays_landlord \
    import TenantPaysLandlord
from model_training.regression.single_output_regression.additional_indemnity import AdditionalIndemnity
from feature_extraction.post_processing.regex.regex_tagger import TagPrecedents


class MultiOutputRegression:
    classifier_labels = MultiClassSVM.load_classifier_labels()
    index = TagPrecedents().get_intent_index()

    def __init__(self, dataset=None):
        """
        Constructor
        :param data_set: [{
            name: 'AZ-XXXXXXX.txt',
            demands_vector: [...],
            facts_vector: [...],
            outcomes_vector: [...]
        },
        {
            ...
        }]
        """
        self.dataset = dataset
        self.monthly_payment_index = -1
        self.months_unpaid_index = -1
        for tuple in MultiOutputRegression.index['facts_vector']:
            if tuple[1] == 'tenant_not_paid_lease_timespan':
                self.months_unpaid_index = tuple[0]
            elif tuple[1] == 'tenant_monthly_payment':
                self.monthly_payment_index = tuple[0]

    def train(self):
        """

        Trains all models
        Simply insert your regression model --> train --> save

        The index of the outcome may change over time so for this reason,
        iterate all the columns of 1 outcome and see if its label matches
        the regression we are trying to perform. Pass that index to the
        constructor so that the regression training knows which column to use.

        :return: None
        """
        outcomes = self.dataset[0]['outcomes_vector']
        for i in range(len(outcomes)):
            try:
                column_name = MultiOutputRegression.classifier_labels[i][0]
            except KeyError:
                MultiOutputRegression.classifier_labels = MultiClassSVM.load_classifier_labels()
                column_name = MultiOutputRegression.classifier_labels[i][0]

            if column_name == 'additional_indemnity_money':
                pass

            elif column_name == 'tenant_ordered_to_pay_landlord':
                regression = TenantPaysLandlord(self.dataset, i)
                regression.train()
                regression.save()

            elif column_name == 'tenant_ordered_to_pay_landlord_legal_fees':
                pass

    def predict(self, facts, outcomes):
        """
        1) Iterate each column. If the column represents an integer data type
           AND it's boolean value == 1 then run it through the regressor.

        2) If 1) is true, then replace the value in the vector by it's true integer
           value.

        Additional notes: step 2) only applies when the boolean value of the classifier
                          returns True. The reason is that the regressor is trained on biased
                          inputs. In a sense, the classifier serves a filtering layer to know
                          which fields are needed by the regressor.

        :param facts: np.array([1, 0, 1, 1, ...])
        :param outcomes: np.array([1, 0, 0, 1, 1, ...])
        :return: np.array([1, 0, 22, 2, ...])
        """
        for i in range(len(outcomes)):
            if outcomes[i] == 1:
                column_name = MultiOutputRegression.classifier_labels[i][0]
                if column_name == 'additional_indemnity_money':
                    monthly_payment = facts[self.monthly_payment_index]
                    months = facts[self.months_unpaid_index]
                    outcomes[i] = AdditionalIndemnity().predict(monthly_payment, months)
                elif column_name == 'tenant_ordered_to_pay_landlord':
                    outcomes[i] = TenantPaysLandlord().predict(facts)[0][0]
                elif column_name == 'tenant_ordered_to_pay_landlord_legal_fees':
                    outcomes[i] = 80

        return outcomes