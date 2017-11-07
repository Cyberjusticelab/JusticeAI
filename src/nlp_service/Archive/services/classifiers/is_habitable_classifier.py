# -*- coding: utf-8 -*-
import os

from Archive.services.classifiers.gram_classifier import GramClassifier


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
