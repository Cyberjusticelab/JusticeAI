# -*- coding: utf-8 -*-
from services.gram_classifier import GramClassifier
import os


class LeaseTermTypeClassifier(GramClassifier):
    inputFiles = ['fixed', 'indeterminate']

    """docstring for LeaseTermTypeClassifier"""

    def __init__(self, forceTrain=False):
        baseName = os.path.basename(__file__).split(".")[0]
        super().__init__(baseName,
                         LeaseTermTypeClassifier.inputFiles,
                         forceTrain)

    def classify(self, questionInput):
        output = super().classify(questionInput)
        return {'lease_term_type': output}
