class IntentModel:
    def __init__(self):
        self.intent_dict = {
            "text": "",
            "intent": "",
            "entities": [
                {
                    "start": "",
                    "end": "",
                    "value": "chinese",
                    "entity": "cuisine",
                    "extractor": "ner_mitie",
                }
            ]
        }
