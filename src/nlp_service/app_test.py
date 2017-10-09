import app


def test_hello():
    assert app.hello() == \
            "Hello World! From the Natural Language Processing Microservice"
