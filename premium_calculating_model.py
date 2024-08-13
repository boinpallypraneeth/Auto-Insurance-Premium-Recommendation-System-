import sys
import json
sys.path.append('/Users/pranavt/Desktop/Insurance Recommendation System/lib/')  
from dgalPy import all


with open('/Users/pranavt/Desktop/Insurance Recommendation System/Car_data/car_value.json', 'r') as file:
    car_data = json.load(file)

def calculate_premiums(base_prices, risk_score, driver_files):
    vehicle_details={}
    with open(driver_files, 'r') as file:
        driver_data = json.load(file)


    # Extract vehicle model from the driver data
    model = driver_data['vehicle_information']['make'] + " " + driver_data['vehicle_information']['model']
    vehicle_details = car_data['Car Models'].get(model, {})

    #print(vehicle_details)
    market_value = vehicle_details.get('Market Value', 0)
    major_repair_cost = vehicle_details.get('Repair Costs', {}).get('Major', 0)

    safe_driving_points = driver_data['history']['safe_driving_points']['total_safe_points']
    annual_mileage = driver_data['vehicle_information'].get('annual_mileage', 0)
    number_of_safety_features = len(driver_data['vehicle_information'].get('safety_features', []))

    # Discount conditions
    moderate_discount_conditions = [
        risk_score > 10 and risk_score <= 14,
        annual_mileage < 15000,
        number_of_safety_features >= 2,
        safe_driving_points>=2
    ]

    low_discount_conditions = [
        risk_score <= 10,
        annual_mileage < 10000,
        number_of_safety_features >= 2,
        safe_driving_points>=1
    ]

    # Evaluate discount conditions using all function from dgal
    apply_moderate_discount = all(moderate_discount_conditions)
    apply_low_discount = all(low_discount_conditions)

    #Applying Discounts
    discount_factor = 1.0
    discount_applied = apply_moderate_discount or apply_low_discount 
    if apply_moderate_discount:
        discount_factor = 0.95
    elif apply_low_discount:
        discount_factor = 0.9

    # Adding the risk score factor
    premiums = {}
    for insurance_type, base_price in base_prices.items():
        if risk_score <= 10:
            premiums_adjustment_risk_score = 1.15
        elif risk_score <= 14:
            premiums_adjustment_risk_score = 1.35
        elif risk_score <= 18:
            premiums_adjustment_risk_score = 1.55
        else:
            premiums_adjustment_risk_score = 1.9

        calculated_premium = base_price * premiums_adjustment_risk_score * discount_factor
        premiums[insurance_type] = f"${calculated_premium:.2f}"

    if major_repair_cost <= 3000 and market_value <= 15000:
        if "liability+collision" in premiums:
            premiums["liability+collision"] = f"${float(premiums['liability+collision'][1:]) * 0.93:.2f}"
        if "liability+collision+comprehensive" in premiums:
            premiums["liability+collision+comprehensive"] = f"${float(premiums['liability+collision+comprehensive'][1:]) * 0.95:.2f}"


    output = {
        "premiums": premiums,
        "discount_applied": discount_applied  
    }

    return output
