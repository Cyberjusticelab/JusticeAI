# -*- coding: utf-8 -*-
from models.question import QuestionOutput
from services.gram_classifier import GramClassifier

class ProblemCategoryClassifier(GramClassifier):
    inputFiles = ['deposits', 'lease_termination', 'nonpayment', 'rent_change']

    """docstring for ProblemCategoryClassifier"""
    def __init__(self):
        super().__init__(ProblemCategoryClassifier.inputFiles)

    def classify(self, questionInput):
        output = super().classify(questionInput.answerString)
        return QuestionOutput(None, None, [{'category': output}])
