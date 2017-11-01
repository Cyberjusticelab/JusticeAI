from src.ml_service import app


def test_hello():
    assert app.hello() == \
        "Hello World! From the Machine Learning Microservice"
