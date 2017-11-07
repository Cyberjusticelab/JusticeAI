from Archive.models.classifier import IntroductionOutput


class IntroductionParser(object):
    """docstring for IntroductionParser"""

    def classify(introduction):
        personClass = 'unknown'
        if introduction.personClassString == "test":
            personClass = 'landlord'
        else:
            personClass = 'tenant'

        return IntroductionOutput(
            introduction.conversationID,
            'Jackie Chan',
            personClass
        )
