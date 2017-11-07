from services.classifiers.tenant_landlord_classifier import TenantLandlordClassifier


def test_classify_tenant():
    assert TenantLandlordClassifier().classify('I am a tenant')[
        'tenant_landlord'] == 'tenant'


def test_classify_landlord():
    assert TenantLandlordClassifier().classify('I am a landlord')[
        'tenant_landlord'] == 'landlord'
