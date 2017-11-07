from Archive.services import IsTenantDeadClassifier


def test_classify_true():
    assert IsTenantDeadClassifier().classify('My tenant is dead')[
        'is_tenant_dead'] == 'true'


def test_classify_false():
    assert IsTenantDeadClassifier().classify('My tenant is alive')[
        'is_tenant_dead'] == 'false'
