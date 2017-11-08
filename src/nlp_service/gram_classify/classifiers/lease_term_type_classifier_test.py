from gram_classify.classifiers.lease_term_type_classifier import LeaseTermTypeClassifier


def test_classify_indeterminate():
    assert LeaseTermTypeClassifier().classify(
        'My lease does not have an end date')[
               'lease_term_type'] == 'indeterminate'


def test_classify_fixed():
    assert LeaseTermTypeClassifier().classify('My lease ends next month')[
               'lease_term_type'] == 'fixed'
