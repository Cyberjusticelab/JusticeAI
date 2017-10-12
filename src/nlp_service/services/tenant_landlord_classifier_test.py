from services.tenant_landlord_classifier import TenantLandlordClassifier


def test_classify_tenant():
    assert TenantLandlordClassifier().classify('I am a tenant')['person_class'] == 'tenant'

def test_classify_landlord():
    assert TenantLandlordClassifier().classify('I am a landlord')['person_class'] == 'landlord'
