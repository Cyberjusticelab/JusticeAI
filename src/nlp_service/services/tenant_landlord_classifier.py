# -*- coding: utf-8 -*-
from textblob import TextBlob
from gram_classifier import GramClassifier
import nltk
import random

class TenantLandlordClassifier(GramClassifier):
    inputFiles = ['tenant', 'landlord']

    """docstring for TenantLandlordClassifier"""
    def __init__(self):
        super().__init__(TenantLandlordClassifier.inputFiles)
