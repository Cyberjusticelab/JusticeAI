# -*- coding: utf-8 -*-
from services.gram_classifier import GramClassifier
import os


class IsHabitableClassifier(GramClassifier):
    inputFiles = ['true', 'false']

    """docstring for IsHabitableClassifier"""

    def __init__(self, forceTrain=False):
        baseName = os.path.basename(__file__).split(".")[0]
        super().__init__(baseName,
                         IsHabitableClassifier.inputFiles,
                         forceTrain)

    def classify(self, questionInput):
        output = super().classify(questionInput)
        return {'is_habitable': output}
