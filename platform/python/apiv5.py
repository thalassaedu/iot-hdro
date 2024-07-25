from flask import Flask, request

app = Flask(__name__)

# Store raw data in memory
received_data = []

@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.data.decode('utf-8')
    if not data:
        return {'error': 'Invalid data format'}, 400

    # Append raw data to the in-memory list
    received_data.append(data)
    print("Received data:", data)
    return {'status': 'success'}, 200

@app.route('/data', methods=['GET'])
def get_data():
    return '<br>'.join(received_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
