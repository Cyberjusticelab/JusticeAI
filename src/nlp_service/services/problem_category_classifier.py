# -*- coding: utf-8 -*-
from textblob import TextBlob
from gram_classifier import GramClassifier
import nltk
import random

class ProblemCategoryClassifier(GramClassifier):
    inputFiles = ['deposits', 'lease_termination', 'nonpayment', 'rent_change']
    """docstring for ProblemCategoryClassifier"""
    def __init__(self):
        super().__init__(ProblemCategoryClassifier.inputFiles)
