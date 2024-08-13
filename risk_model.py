import json
from datetime import datetime

with open('/Users/pranavt/Desktop/Insurance Recommendation System/Payment History/credit_history.json', 'r') as file:
    payment_data = json.load(file)
with open('/Users/pranavt/Desktop/Insurance Recommendation System/Claims History/claims_history.json', 'r') as file:
    claims_data = json.load(file)
with open('/Users/pranavt/Desktop/Insurance Recommendation System/Car_data/car_value.json', 'r') as file:
    car_values_data = json.load(file)['Car Models']
with open('/Users/pranavt/Desktop/Insurance Recommendation System/carfax/carfax_report.json', 'r') as file:
    carfax_data = json.load(file)['carfax_reports']
#Calculating risk factor based on the intervals between incident dates(Frequency between incidents from driver's driving history)
def calculate_interval_factor(dates):
    dates = sorted([datetime.strptime(date, "%Y-%m-%d") for date in dates])
    intervals = []
    for i in range(1, len(dates)):
        interval = (dates[i] - dates[i-1]).days
        if interval < 180:
            intervals.append(1.5)
        elif interval < 365:
            intervals.append(1.0)
        else:
            intervals.append(0.5)
    return sum(intervals)

#Calculating payment risk from the drivers payment history that is from his credit score
def calculate_payment_history_risk(credit_score, monthly_payments_on_time):
    payment_risk = 0
    if credit_score >= 750:
        payment_risk -= 0.05  
    elif 700 <= credit_score < 750:
        payment_risk -= 0.02
    else:
            if monthly_payments_on_time:
                payment_risk -= 0.01
            else:
                payment_risk += 0.05  

    return payment_risk

#Calculating location risk from the location in which driver drives his car
def calculate_location_risk(location):
    risk = 0
    location_type = location.get('type', '')
    population_density = location.get('population_density', '')
    crime_rate = location.get('crime_rate', '')

    if location_type == 'Urban':
        if population_density == 'High':
            risk += 0.1
        elif population_density == 'Medium':
            risk += 0.05
    elif location_type == 'Suburban':
        if population_density == 'High':
            risk += 0.07
        elif population_density == 'Medium':
            risk += 0.04
    elif location_type == 'Rural':
        if population_density == 'Low':
            risk += 0.02

    if crime_rate == 'High':
        risk += 0.05
    elif crime_rate == 'Moderate':
        risk += 0.03
    elif crime_rate == 'Low':
        risk += 0.01

    return risk



#Calculating age
def calculate_age(dob):
    birthdate = datetime.strptime(dob, "%Y-%m-%d")
    today = datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

#Calculating age risk
def calculate_age_risk(age):
    if age < 23:
        return 2.0  
    elif age < 35:
        return 1.0  
    elif age > 65:
        return 1.5  
    else:
        return 0

#Calculating weighted claims risk
def calculate_weighted_claims_risk(claims, years_insured):
    minor_claim_impact = 0.4
    total_loss_impact = 1.0

    if years_insured >= 3:
        minor_claim_impact *= 0.8
        total_loss_impact *= 0.7
    else:
        minor_claim_impact *= 1.2
        total_loss_impact *= 1.1

    risk_from_claims = (claims['minor_claims'] * minor_claim_impact +
                        claims['total_loss'] * total_loss_impact)
    return risk_from_claims

#verifying whether we  have the carfax report for the car
def find_carfax_report(vin, carfax_reports):
    for report in carfax_reports:
        if report['vin'] == vin:
            return report
    return None


#Vehicle Risk
def calculate_vehicle_risk(vehicle_info, carfax_report, car_values):
    model_key = f"{vehicle_info['make']} {vehicle_info['model']}"
    car_model_data = car_values.get(model_key, {})
    risk_score = 0
    current_year = datetime.now().year
    vehicle_age = current_year - vehicle_info['year']
    annual_mileage = vehicle_info.get('annual_mileage', 12000)  # Default to 12000 if not specified
    current_mileage = carfax_report.get('current_mileage', {}).get('mileage', 0)


    if current_mileage > 15000: 
        risk_score += 0.5


    if annual_mileage>15000:
        risk_score+=0.5
    

    if vehicle_age>5:
        risk_score+=0.5
    
    # Evaluating  service records
    service_records = carfax_report.get('service_history', {}).get('service_records', 0)
    if service_records <= 5:
        risk_score += 0.4 
    

    if carfax_report:
        # Accessing  accident history
        major_accidents = carfax_report['accident_history'].get('major_accidents', 0)
        minor_accidents = carfax_report['accident_history'].get('minor_accidents', 0)
        
        # Adjusting risk score based on the number of accidents
        risk_score += major_accidents * 0.8  # Major accidens increases risk more significantly
        risk_score += minor_accidents * 0.4 
    
    # Adjusting risk based on repair history and cost
    if car_model_data:
        # Determining the max thresholds for repair costs
        high_major_repair_threshold = car_model_data['Repair Costs']['Major'] * 1.2  # Considering 20% above average from our data
        high_minor_repair_threshold = car_model_data['Repair Costs']['Minor'] * 1.2  # Considering 20% above average
            
        # Calculating actual repair costs
        actual_major_repairs_cost = carfax_report['repair_history']['major_repairs'] * car_model_data['Repair Costs']['Major']
        actual_minor_repairs_cost = carfax_report['repair_history']['minor_repairs'] * car_model_data['Repair Costs']['Minor']
            
        # Checking  if actual repair counts and costs exceed thresholds
        if carfax_report['repair_history']['major_repairs'] > 2:
            if actual_major_repairs_cost > high_major_repair_threshold:
                excess_percentage = (actual_major_repairs_cost - high_major_repair_threshold) / high_major_repair_threshold
                risk_score += excess_percentage * 2 

        if carfax_report['repair_history']['minor_repairs'] > 2:
            if actual_minor_repairs_cost > high_minor_repair_threshold:
                excess_percentage = (actual_minor_repairs_cost - high_minor_repair_threshold) / high_minor_repair_threshold
                risk_score += excess_percentage * 1 


    # Title status impact
    title_status = carfax_report.get('title_status', 'Clean')
    if title_status == 'Rebuilt':
        risk_score += 0.5  # Increasing the risk if title is rebuilt
    
    # Assesing the Safety features
    safety_features = vehicle_info.get('safety_features', [])
    num_safety_features = len(safety_features)
    if num_safety_features == 3:
        risk_score -= 1  
    elif num_safety_features == 2:
        risk_score -= 0.7 
    elif num_safety_features == 1:
        risk_score -= 0.3  
    else:
        risk_score += 0.5


    return risk_score


#Calculating overall risk score
def calculate_risk_score(data):
    driver_license_number = data['driver_information']['driver_license_number']

    #Payment history risk
    driver_payment_history = next((item for item in payment_data if item['driver_license_number'] == driver_license_number), None)
    credit_score = driver_payment_history['credit_score'] if driver_payment_history else 700
    monthly_payments_on_time = driver_payment_history['monthly_payments_on_time'] if driver_payment_history else True
    payment_history_risk = calculate_payment_history_risk(credit_score, monthly_payments_on_time)

    #Claims history risk
    driver_claims_history = next((item for item in claims_data if item['driver_license_number'] == driver_license_number), None)
    previous_claims = driver_claims_history['previous_claims'] if driver_claims_history else {'minor_claims': 0, 'total_loss': 0}
    years_insured = data.get('insured_for', 0)
    claims_risk = calculate_weighted_claims_risk(previous_claims, years_insured)

    #Vehicle Risk
    vehicle_info = data.get('vehicle_information')
    if vehicle_info and 'vin' in vehicle_info:
        carfax_report = find_carfax_report(vehicle_info['vin'], carfax_data)
        vehicle_risk = calculate_vehicle_risk(vehicle_info, carfax_report, car_values_data)
    else:
        vehicle_risk = 0 

    #age risk
    age = calculate_age(data['driver_information']['date_of_birth'])
    age_risk = calculate_age_risk(age)

    #Traffic violations, accidents and suspensions risk
    violation_dates = [violation['date'] for violation in data['violations']]
    accident_dates = [accident['date'] for accident in data['accidents'] if accident['at_fault'] == "Yes"]
    suspension_dates = [suspension['date'] for suspension in data['history']['suspensions']]
    all_dates = violation_dates + accident_dates + suspension_dates
    if all_dates:
        interval_factor = calculate_interval_factor(all_dates)
    else:
        interval_factor = 0
    base_points = sum(v['points'] for v in data['violations']) + \
                  sum(a['points'] for a in data['accidents'] if a['at_fault'] == "Yes") + \
                  sum(s['points'] for s in data['history']['suspensions'])
    safe_driving_points = data['history'].get('safe_driving_points', {}).get('total_safe_points', 0)

    #Location risk
    location_risk = calculate_location_risk(data.get('location', {}))

    #Net points
    net_points = max(0, base_points - safe_driving_points) + interval_factor

    #By adding all other risks
    total_risk_score = net_points + payment_history_risk + location_risk + age_risk + vehicle_risk + claims_risk

    #performing features scaling
    return round(total_risk_score*0.8,2)



#Calculating risk for each and every driver
def process_driver_data(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    risk_score = calculate_risk_score(data)
    risk_level = 'Low Risk' if risk_score <= 10 else 'Moderate Risk' if risk_score <= 14 else 'High Risk' if risk_score <= 18 else 'Very High Risk'

    vehicle_info=data.get("vehicle_information",{})
    return {
        "driver_information": data["driver_information"],
        "license_status": data["license_status"],
        "vehicle_information": vehicle_info,
        "risk_score": risk_score,
        "risk_level": risk_level
    }