import random


class FactService:
    fact_dict = {
        "lease_termination": {
            "lease_term_type": ["Is there a specified end date to your lease?"],
            "has_lease_expired": ["Has the lease expired already?"],
            "is_tenant_dead": ["Is the tenant dead?"],
            "is_student": ["Are you a student?"],
            "is_habitable": ["How would you describe your dwelling? Is it habitable?"]
        },
        "rent_change": {
            "lease_term_type": ["Is there a specified end date to your lease?"],
            "is_rent_in_lease": ["Is the rent specified in the lease?"],
            "rent_in_lease_amount": ["What is the amount of the rent"]
        },
        "nonpayment": {
            "in_default": ["How long has it been since you haven't paid?"],
            "over_three_weeks": ["Has payment not been made in over three weeks?"],
            "has_abandoned": ["Have you seen your tenant?"],
        },
        "deposits": {
            "is_rent_advance": ["Has the rent been asked to be paid in advance?"],
            "first_month_rent_paid": ["Is it only for the first month?"]
        }
    }

    @staticmethod
    def get_question(claim_category, facts_resolved):
        all_category_facts = list(FactService.fact_dict[claim_category])
        facts_unresolved = [x for x in all_category_facts if x not in facts_resolved]

        # Pick the first unresolved fact, return None if none remain
        if len(facts_unresolved) == 0:
            return None, None

        fact = facts_unresolved[0]

        choice = random.choice  # For random question choice
        question = choice(FactService.fact_dict[claim_category][fact])

        return fact, question
