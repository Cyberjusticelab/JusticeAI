import json
from web import ml_controller
from numpy.testing import assert_array_equal


def test__dict_to_vector():
    # Test data
    test_json = """
    {
      "demands" : {
        "demand_lease_modification": 1,
        "demand_resiliation": 1,
        "landlord_claim_interest_damage": 0,
        "landlord_demand_access_rental": 1,
        "landlord_demand_bank_fee": 1,
        "landlord_demand_damage": 1,
        "landlord_demand_legal_fees": 1,
        "landlord_demand_retake_apartment": 1,
        "landlord_demand_utility_fee": 1,
        "landlord_fix_rent": 1,
        "landlord_lease_termination": 1,
        "landlord_money_cover_rent": 1,
        "paid_judicial_fees": 1,
        "tenant_claims_harassment": 0,
        "tenant_cover_rent": 1,
        "tenant_demands_decision_retraction": 1,
        "tenant_demand_indemnity_Code_Civil": 1,
        "tenant_demand_indemnity_damage": 1,
        "tenant_demand_indemnity_judicial_fee": 1,
        "tenant_demand_interest_damage": 1,
        "tenant_demands_money": 1,
        "tenant_demand_rent_decrease": 1,
        "tenant_respect_of_contract": 1,
        "tenant_eviction": 0
      }
    }
    """
    input_json = json.loads(test_json)

    # Execute
    result = ml_controller.__dict_to_vector(
        input_json['demands'], 'demands_vector')

    # Verify
    assert_array_equal(result, [1.,  1.,  0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                                0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.])
