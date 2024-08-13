import json
from copy import deepcopy
from risk_model import process_driver_data
from base_price import calculate_base_prices
from premium_calculating_model import calculate_premiums

def main():
    base_path = "/Users/pranavt/Desktop/Insurance Recommendation System/Driver_data/"
    driver_files = [base_path + f"driver_{i}.json" for i in range(1, 11)]
    risk_results = []
    premiums_output = [] 


    file_path = '/Users/pranavt/Desktop/Insurance Recommendation System/Insurance Company data/company.json'
    with open(file_path, 'r') as file:
        data = json.load(file)


    monthly_prices = calculate_base_prices(data) 


    for driver_file in driver_files:
        driver_result = process_driver_data(driver_file)  
        premiums = calculate_premiums(
            monthly_prices, 
            driver_result['risk_score'],
            driver_file  
        )
        risk_results.append(deepcopy(driver_result))  
        driver_result['premiums'] = premiums
        premiums_output.append({
            **driver_result['driver_information'], 
            'vehicle_information': driver_result['vehicle_information'],
            'risk_score': driver_result['risk_score'], 
            'premiums': premiums
        })

    # Save the results with risk score
    with open('/Users/pranavt/Desktop/Insurance Recommendation System/risk_output.json', 'w') as outfile:
        json.dump(risk_results, outfile, indent=4)

    # Save the results with premium outputs
    with open('/Users/pranavt/Desktop/Insurance Recommendation System/premium_calculation_output.json', 'w') as outfile:
        json.dump(premiums_output, outfile, indent=4)

if __name__ == "__main__":
    main()
