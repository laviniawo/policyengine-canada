from policyengine_canada.model_api import *


class qc_fa_supplement(Variable):
    value_type = float
    entity = Household
    label = "Quebec family allowance supplements"
    definition_period = YEAR
    defined_for = ProvinceCode.QC

    def formula(household, period, parameters):
        p = parameters(period).gov.provinces.qc.tax.income.credits.fa

        person = household.members

        # Supplement for the Purchase of School Supplies
        age = person["age", period]
        supplement_school_supplies = p.school_supplies_amount.calc(age)

        # Supplement for Handicapped Children
        handicapped = person["is_disabled", period]
        supplement_handicapped = (
            handicapped * p.handicapped_child_supplement.base_amount
        )

        # Supplement for Handicapped Children Requiring Exceptional Care
        handicapped_tier1 = person["qc_fa_exceptional_care_tier1", period]
        supplement_handicapped_tier1 = (
            handicapped
            * handicapped_tier1
            * p.handicapped_child_supplement.exceptional_care_tier1_amount
        )

        handicapped_tier2 = person["qc_fa_exceptional_care_tier2", period]
        supplement_handicapped_tier2 = (
            handicapped
            * handicapped_tier2
            * p.handicapped_child_supplement.exceptional_care_tier2_amount
        )

        supplements = (
            supplement_school_supplies
            + supplement_handicapped
            + supplement_handicapped_tier1
            + supplement_handicapped_tier2
        )

        return household.sum(supplements)
