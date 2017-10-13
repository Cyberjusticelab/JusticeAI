# -*- coding: utf-8 -*-
from services.gram_classifier import GramClassifier
import os


class TenantLandlordClassifier(GramClassifier):
    inputFiles = ['tenant', 'landlord']

    """docstring for TenantLandlordClassifier"""

    def __init__(self, forceTrain=False):
        baseName = os.path.basename(__file__).split(".")[0]
        super().__init__(baseName,
                         TenantLandlordClassifier.inputFiles,
                         forceTrain)

    def classify(self, questionInput):
        output = super().classify(questionInput)
        return {'tenant_landlord': output}
