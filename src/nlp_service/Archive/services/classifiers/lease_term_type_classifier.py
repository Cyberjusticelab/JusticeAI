# -*- coding: utf-8 -*-
import os

from Archive.services.classifiers.gram_classifier import GramClassifier


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
