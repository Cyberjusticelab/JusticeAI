from model_training.regression.single_output_regression.tenant_pays_landlord_regressor \
    import TenantPaysLandlordRegressor
from model_training.classifier.multi_class_svm import MultiClassSVM


class MultiOutputRegression:
    classifier_labels = MultiClassSVM.load_classifier_labels()

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

    def train(self):
        """
        Trains all models
        Simply insert your regression model --> train --> save
        :return: None
        """
        regression = TenantPaysLandlordRegressor(self.dataset)
        regression.train()
        regression.save()

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

                if column_name == 'additional_indemnity_date':
                    pass
                elif column_name == 'additional_indemnity_money':
                    pass
                elif column_name == 'tenant_ordered_to_pay_landlord':
                    outcomes[i] = TenantPaysLandlordRegressor().predict(facts)[0][0]
                elif column_name == 'tenant_ordered_to_pay_landlord_legal_fees':
                    pass

        return outcomes
