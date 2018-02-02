class RegexModel:
    def __init__(self):
        # escape forward slash
        self.regex_dict = {
        }

    def name(self, data):
        if data is not "":
            self.regex_dict['name'] = data

    def pattern(self, data):
        if data is not "":
            self.regex_dict['pattern'] = data
