from flask import Flask, request, jsonify
import mysql.connector
import json

app = Flask(__name__)

# MySQL database connection configuration
db_config = {
    'user': 'root',
    'password': 'test1234',
    'host': '192.168.2.221',
    'database': 'sensor_data_db',
    'port': 30036  # Specify the custom port for MySQL
}

# Create a MySQL database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
