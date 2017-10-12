from services.has_lease_expired_classifier import HasLeaseExpiredClassifier


def test_classify_false():
    assert HasLeaseExpiredClassifier().classify(
      'My lease ends in a few months')[
        'has_lease_expired'] == 'false'


def test_classify_true():
    assert HasLeaseExpiredClassifier().classify('My lease has expired')[
        'has_lease_expired'] == 'true'
