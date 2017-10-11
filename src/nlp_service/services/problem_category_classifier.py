# -*- coding: utf-8 -*-
from models.question import QuestionOutput
from services.gram_classifier import GramClassifier
import os


class ProblemCategoryClassifier(GramClassifier):
    inputFiles = ['deposits', 'lease_termination', 'nonpayment', 'rent_change']

    """docstring for ProblemCategoryClassifier"""

    def __init__(self):
        baseName = os.path.basename(__file__).split(".")[0]
        super().__init__(baseName, ProblemCategoryClassifier.inputFiles)

    def classify(self, questionInput):
        output = super().classify(questionInput.answerString)
        return QuestionOutput(None, None, [{'category': output}])
