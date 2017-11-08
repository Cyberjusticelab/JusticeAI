from gram_classify.classifiers.problem_category_classifier import ProblemCategoryClassifier


def test_classify_lease_termination():
    assert ProblemCategoryClassifier().classify(
        'I would like to terminate my lease')[
               'category'] == 'lease_termination'


def test_classify_deposits():
    assert ProblemCategoryClassifier().classify(
        'My landlord wants a month in advance')['category'] == 'deposits'


def test_classify_nonpayment():
    assert ProblemCategoryClassifier().classify(
        'My tenant hasn\'t paid me in a month')['category'] == 'nonpayment'


def test_classify_rent_change():
    assert ProblemCategoryClassifier().classify(
        'My landlord wants to increase the rent')['category'] == 'rent_change'
