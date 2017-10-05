class QuestionInput(object):
    """docstring for Question"""

    def __init__(self, questionID, conversationID, answerString):
        self.questionID = questionID
        self.conversationID = conversationID
        self.answerString = answerString
        return


class QuestionOutput(object):
    """docstring for Question"""

    def __init__(self, questionID, conversationID, facts):
        self.questionID = questionID
        self.conversationID = conversationID
        self.facts = facts
        return
