from policyengine_canada.model_api import *


class ns_income_assistance_asset_eligibility(Variable):
    value_type = bool
    entity = Household
    label = "Nova Scotia income assistance asset eligibility"
    definition_period = YEAR
    defined_for = ProvinceCode.NS

    def formula(household, period, parameters):
        household_size = household("household_size",period)
        p = parameters(
            period
        ).gov.provinces.ns.tax.income.income_assistance.eligibility.assets
        max_asset_limit = p.max_assets.calc(household_size)
        ns_applicable_asset_amount = add(household, period, p.applicable_assets)
        return  max_asset_limit >= ns_applicable_asset_amount
