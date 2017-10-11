# -*- coding: utf-8 -*-
from models.question import QuestionOutput
from services.gram_classifier import GramClassifier

class TenantLandlordClassifier(GramClassifier):
    inputFiles = ['tenant', 'landlord']

    """docstring for TenantLandlordClassifier"""
    def __init__(self):
        super().__init__(TenantLandlordClassifier.inputFiles)

    def classify(self, questionInput):
        output = super().classify(questionInput.answerString)
        return QuestionOutput(None, None, [{'person_class': output}])
