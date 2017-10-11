import requests

NLP_URL = "http://0.0.0.0:3002"


def introduction(conversation_id, name, person):
    req_dict = {
        "conversation_id": conversation_id,
        "name": name,
        "person": person
    }
    res = requests.post("{}/{}".format(NLP_URL, "introduction"), json=req_dict)
    return res.json()


def tenant_landlord(answer):
    req_dict = {
        "answer": answer
    }
    res = requests.post("{}/{}".format(NLP_URL, "tenant_landlord"), json=req_dict)
    return res.json()


def problem_category(answer):
    req_dict = {
        "answer": answer
    }
    res = requests.post("{}/{}".format(NLP_URL, "problem_category"), json=req_dict)
    return res.json()


def yesno(question_id, conversation_id, answer):
    req_dict = {
        "question_id": question_id,
        "conversation_id": conversation_id,
        "answer": answer
    }
    res = requests.post("{}/{}".format(NLP_URL, "yesno"), json=req_dict)
    return res.json()
