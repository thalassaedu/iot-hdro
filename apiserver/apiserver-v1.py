from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pymysql
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to allow cross-origin requests

# MySQL database connection configuration
db_config = {
    'user': 'root',
    'password': 'test1234',
    'host': '192.168.2.221',
    'database': 'sensor_data_db',
    'port': 30036  # Specify the custom port for MySQL
}

# Create a MySQL database connection using PyMySQL
def get_db_connection():
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        port=db_config['port'],
        cursorclass=pymysql.cursors.DictCursor
    )

# Endpoint to receive sensor data from ESP32
@app.route('/sensor-data', methods=['POST'])
def receive_sensor_data():
    try:
        data = request.json  # Get JSON data from ESP32
        if not data:
            return jsonify({'message': 'No data received'}), 400

        # Connect to MySQL database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Prepare SQL statement to insert sensor data
        insert_query = """
        INSERT INTO sensor_data (N, P, K, Temperature, Humidity, Lux)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (data['N'], data['P'], data['K'], data['Temperature'], data['Humidity'], data['Lux'])

        # Execute the query and commit changes
        cursor.execute(insert_query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Data inserted successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to insert data', 'error': str(e)}), 500

# Endpoint to retrieve the latest sensor data
@app.route('/latest-sensor-data', methods=['GET'])
def get_latest_sensor_data():
    try:
        # Connect to MySQL database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to fetch the latest sensor data
        query = """
        SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1
        """
        cursor.execute(query)
        latest_data = cursor.fetchone()

        cursor.close()
        connection.close()

        return jsonify(latest_data), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve data', 'error': str(e)}), 500

# Serve the webpage
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
