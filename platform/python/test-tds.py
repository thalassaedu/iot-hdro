from flask import Flask, request, jsonify

app = Flask(__name__)

# Sensor reading to correct water value mapping
sensor_to_water_mapping = {
    25: 75,
    45: 100,
    62: 125,
    85: 150,
    105: 175,
    125: 200,
    145: 225,
    165: 250,
    185: 275,
    205: 300,
    225: 325,
    235: 350,
    250: 375,
    265: 400,
    290: 450,
    321: 500,
    365: 550,
    375: 600,
    425: 650,
    500: 800,
    545: 900,
    600: 1000
}

def get_closest_values(sensor_value):
    # Sort the sensor values
    sorted_keys = sorted(sensor_to_water_mapping.keys())
    
    # Find the two closest sensor values
    lower = None
    upper = None
    for i, key in enumerate(sorted_keys):
        if key == sensor_value:
            return key, None, sensor_to_water_mapping[key]
        elif key > sensor_value:
            upper = key
            lower = sorted_keys[i - 1] if i > 0 else None
            break

    if lower is None:
        lower = sorted_keys[0]
    if upper is None:
        upper = sorted_keys[-1]

    return lower, upper, None

@app.route('/get_water_value', methods=['GET'])
def get_water_value():
    # Get the sensor value from the query parameter
    sensor_value = int(request.args.get('sensor_value'))

    lower, upper, exact_value = get_closest_values(sensor_value)

    if exact_value is not None:
        return jsonify({
            'sensor_value': sensor_value,
            'correct_water_value': exact_value,
            'message': 'Exact match found'
        })

    # Interpolate to find the proportional value
    lower_value = sensor_to_water_mapping[lower]
    upper_value = sensor_to_water_mapping[upper]
    
    interpolated_value = lower_value + ((sensor_value - lower) / (upper - lower)) * (upper_value - lower_value)

    return jsonify({
        'sensor_value': sensor_value,
        'closest_lower_value': lower,
        'closest_upper_value': upper,
        'interpolated_water_value': round(interpolated_value, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
