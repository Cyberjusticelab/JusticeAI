from services.problem_category_classifier import ProblemCategoryClassifier


def test_init():
    assert ProblemCategoryClassifier() is not None
