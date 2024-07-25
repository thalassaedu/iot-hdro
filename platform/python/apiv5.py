from flask import Flask, request

app = Flask(__name__)

# Store raw Arduino data in memory
raw_arduino_data = []

@app.route('/update_arduino', methods=['POST'])
def update_arduino():
    data = request.json.get('data')
    if not data:
        return {'error': 'Invalid data format'}, 400

    # Append raw data to the in-memory list
    raw_arduino_data.append(data)
    print("Received raw data:", data)
    return {'status': 'success'}, 200

@app.route('/arduino-data', methods=['GET'])
def get_arduino_data():
    return '<br>'.join(raw_arduino_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
