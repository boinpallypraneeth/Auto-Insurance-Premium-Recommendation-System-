import json

def calculate_base_prices(data):
    operational_costs = data['operational_costs']
    claim_costs = data['claim_costs']
    profit_margin = data['profit_margin']
    expected_customer_volume = data['expected_customer_volume']
    claim_data = data['claim_frequency_and_severity']

    # Calculating total costs and required revenue
    total_costs = operational_costs + claim_costs
    required_revenue = total_costs / (1 - profit_margin)

    # Calculating  base price per policy
    base_price_per_policy = required_revenue / expected_customer_volume

    # Calculating adjusted base prices for each insurance type
    monthly_prices={}
    for insurance_type, frequency_severity in claim_data.items():
        frequency = frequency_severity['frequency']
        severity = frequency_severity['severity']
        # Expected annual cost per policy
        annual_cost_per_policy = frequency * severity
        #The base price per policy is then adjusted by adding the annual cost per policy calculated from claim data.
        adjusted_annual_price = base_price_per_policy + annual_cost_per_policy
        adjusted_monthly_price = adjusted_annual_price / 12
        monthly_prices[insurance_type] = adjusted_monthly_price
    
    return monthly_prices
    
