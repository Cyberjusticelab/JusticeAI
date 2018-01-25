class SynonymModel:
    def __init__(self):
        self.syn_dict = {}

    def entity(self, data):
        if data is not "":
            self.syn_dict['entity'] = data

    def synonyms(self, data):
        if (data is not "") and (len(data) > 0):
            self.syn_dict['synonyms'] = data