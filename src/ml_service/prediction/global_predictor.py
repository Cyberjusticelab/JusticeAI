from model_training.classifier.multi_class_svm import MultiClassSVM
from model_training.regression.multi_output_regression import MultiOutputRegression


class GlobalPredictor:
    classifier_model = MultiClassSVM()
    regression_model = MultiOutputRegression()

    def __init__(self):
        pass

    @staticmethod
    def predict_outcome(data):
        """
        1)  Use the multi output classifier to create the outcome vector.
            This is a vector of 1's and 0's as shown below:
                [0, 1, 0, 1, ...]

        2) Iterate each column. If the column represents an integer data type
           AND it's boolean value == 1 then run it through the regressor.

        3) If 2) is true, then replace the value in the vector by it's true integer
           value.

        Additional notes: step 2) only applies when the boolean value of the classifier
                          returns True. The reason is that the regressor is trained on biased
                          inputs. In a sense, the classifier serves a filtering layer to know
                          which fields are needed by the regressor.

        :param data: np.array([1, 0, 522, 0, 1, ...])
        :return: np.array([1, 0, 22, 2, ...])
        """
        outcome_vector = GlobalPredictor.classifier_model.predict(data)[0]
        outcome_vector = GlobalPredictor.regression_model.predict(outcome_vector)
        return outcome_vector
