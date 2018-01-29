class MetaDict:
    def __init__(self):
        self.meta = {
        }

    def open(self, data):
        if data is not "":
            self.meta['open'] = data

    def close(self, data):
        if data is not "":
            self.meta['close'] = data

    def entity(self, data):
        if data is not "":
            self.meta['entity'] = data

    def extractor(self, data):
        if data is not "":
            self.meta['extractor'] = data
