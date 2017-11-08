import requests

NLP_URL = "http://nlp_service:3002"


def submit_answer(conversation_id, message):
    req_dict = {
        "conversation_id": conversation_id,
        "message": message
    }
    res = requests.post("{}/{}".format(NLP_URL, "submit_answer"), json=req_dict)
    return res.json()
