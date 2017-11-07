# -*- coding: utf-8 -*-
import os

from Archive.services.classifiers.gram_classifier import GramClassifier


class HasLeaseExpiredClassifier(GramClassifier):
    inputFiles = ['true', 'false']

    """docstring for HasLeaseExpiredClassifier"""

    def __init__(self, forceTrain=False):
        baseName = os.path.basename(__file__).split(".")[0]
        super().__init__(baseName,
                         HasLeaseExpiredClassifier.inputFiles,
                         forceTrain)

    def classify(self, questionInput):
        output = super().classify(questionInput)
        return {'has_lease_expired': output}
