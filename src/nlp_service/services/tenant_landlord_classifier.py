# -*- coding: utf-8 -*-
from models.question import QuestionOutput
from services.gram_classifier import GramClassifier
import os


class TenantLandlordClassifier(GramClassifier):
    inputFiles = ['tenant', 'landlord']

    """docstring for TenantLandlordClassifier"""

    def __init__(self):
        baseName = os.path.basename(__file__).split(".")[0]
        super().__init__(baseName, TenantLandlordClassifier.inputFiles)

    def classify(self, questionInput):
        output = super().classify(questionInput.answerString)
        return QuestionOutput(None, None, [{'person_class': output}])
