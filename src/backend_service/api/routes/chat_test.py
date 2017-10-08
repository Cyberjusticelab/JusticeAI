from api import routes

def test_hello():
    assert routes.chat.hello() == "Hello World! From the Web Backend Microservice!"

