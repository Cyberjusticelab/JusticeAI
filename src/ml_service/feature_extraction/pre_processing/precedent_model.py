class PrecedentModel:
    def __init__(self):
        self.dict = {
            'facts': {
            },
            'decisions': {
            }
        }

    def __str__(self):
        return_str = "Facts:\n"
        for f in self.dict['facts']:
            return_str += str(self.dict['facts'][f])
            return_str += f + '\n\n'

        return_str += 'Decisions:\n'
        for f in self.dict['decisions']:
            return_str += str(self.dict['decisions'][f])
            return_str += f + "\n\n"
        return return_str


class FactModel:
    def __init__(self):
        self.dict = {
            'fact': None,
            'precedence': [],
            'vector': None
        }

    def __str__(self):
        return str(self.dict['precedence']) + '\n' + \
            str(self.dict['fact'])
