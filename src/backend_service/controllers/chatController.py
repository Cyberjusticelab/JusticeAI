from flask import jsonify
from models.Claim import Claim

tempDB = {}


def init_claim(name):
    claim = Claim(name)
    # DB stuff here
    tempDB[claim.id] = claim
    return jsonify(
        {
            'name': claim.name,
            'claim_id': claim.id
        }
    )


def chat_message(claim_id, answer):
    claim = tempDB[claim_id]
    claim.add_answer(answer)

    question = "Hello there %s, this is question #%s" % (claim.name, str(len(claim.questions)))
    claim.add_question(question)

    return jsonify(
        {
            'claim_id': claim_id,
            'questions': claim.questions,
            'answers': claim.answers,
            'message': question,
        }
    )
