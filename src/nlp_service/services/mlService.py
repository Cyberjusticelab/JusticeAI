import requests

ML_URL = "http://ml_service:3001"


# This is a placeholder until the interface for the ML service is defined.
def submit_resolved_fact(conversation_id, current_fact, entity_value):
    req_dict = {
        "conversation_id": conversation_id,
        "fact_id": current_fact.id,
        "entity_value": entity_value
    }
    res = requests.post("{}/{}".format(ML_URL, "process"), json=req_dict)
    return res.json()
