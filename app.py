import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_vehicle_specs(year, make, model):
    """
    Query the NHTSA API (GetCanadianVehicleSpecifications endpoint) for vehicle specifications.
    """
    url = (
        f"https://vpic.nhtsa.dot.gov/api/vehicles/GetCanadianVehicleSpecifications/"
        f"?year={year}&make={make}&model={model}&format=json"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error: Received status code {response.status_code}")
    try:
        data = response.json()
    except Exception as e:
        raise Exception(f"Error decoding JSON: {e}")
    return data


def get_vehicle_weight(year, make, model, specific_model=None):
    """
    Retrieves the vehicle's weight (CW) from the API.
    """
    data = get_vehicle_specs(year, make, model)
    count = data.get("Count", 0)
    results = data.get("Results", [])
    if count == 0 or not results:
        raise Exception("No data found for the specified vehicle")
    selected_result = None
    if count > 1 and specific_model:
        for res in results:
            specs = res.get("Specs", [])
            model_value = None
            for spec in specs:
                if spec.get("Name", "").lower() == "model":
                    model_value = spec.get("Value", "").strip().lower()
                    break
            if model_value and specific_model.lower() in model_value:
                selected_result = res
                break
        if selected_result is None:
            selected_result = results[0]
    else:
        selected_result = results[0]
    weight_value = None
    for spec in selected_result.get("Specs", []):
        if spec.get("Name", "").upper() == "CW":
            weight_value = spec.get("Value", None)
            break
    if weight_value is None:
        raise Exception("Weight (CW) not found in the specifications")
    try:
        weight_value = float(weight_value)
    except ValueError:
        raise Exception("Weight value is not a valid number")
    return round(weight_value * 0.001102, 1)


@app.route('/get_vehicle_weight', methods=['GET'])
def api_get_vehicle_weight():
    year = request.args.get('year')
    make = request.args.get('make')
    model = request.args.get('model')
    isOntario = request.args.get('isOntario')
    
    if not (year and make and model and isOntario):
        return jsonify({"error": "Missing required parameters: year, make, model"}), 400

    try:
        year = int(year)
    except ValueError:
        return jsonify({"error": "Invalid year parameter"}), 400

    try:
        weight = get_vehicle_weight(year, make, model, specific_model=None)
        if isOnatario:
            rate = 220
            price = 220 * weight
            return jsonify({"results": {"scrap_price": price}})
        else:
            rate = 120
            price = 120 * weight
            return jsonify({"results": {"scrap_price": price}})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
