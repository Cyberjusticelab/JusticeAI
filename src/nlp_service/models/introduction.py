class IntroductionInput(object):
    """docstring for Introduction"""

    def __init__(self, conversationID, nameString, personClassString):
        self.conversationID = conversationID
        self.nameString = nameString
        self.personClassString = personClassString
        return


class IntroductionOutput(object):
    """docstring for Introduction"""

    def __init__(self, conversationID, name, personClass):
        self.conversationID = conversationID
        self.name = name
        self.personClass = personClass
        return
