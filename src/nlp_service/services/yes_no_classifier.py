from models.question import QuestionOutput


class YesNoClassifier(object):
    """docstring for YesNoClassifier"""

    def classify(question):
        facts = []
        if question.answerString == "yes":
            facts.append('positive')
        else:
            facts.append('negative')

        return QuestionOutput(
            question.questionID,
            question.conversationID,
            facts
        )
