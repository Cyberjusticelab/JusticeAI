import requests

#NLP_URL = "http://nlp_service:3002"
NLP_URL = "http://127.0.0.1:3002"

def claim_category(conversation_id, message):
    req_dict = {
        "conversation_id": conversation_id,
        "message": message
    }
    res = requests.post("{}/{}".format(NLP_URL, "claim_category"), json=req_dict)
    return res.json()


def submit_message(conversation_id, message):
    req_dict = {
        "conversation_id": conversation_id,
        "message": message
    }
    res = requests.post("{}/{}".format(NLP_URL, "submit_message"), json=req_dict)
    return res.json()
