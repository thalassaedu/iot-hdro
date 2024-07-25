from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

MYSQL_HOST = '192.168.2.194'
MYSQL_PORT = 30036
MYSQL_DATABASE = 'sensor_data'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'test1234'

# Store raw data in memory
received_data = []

def insert_sensor_data(temperature, humidity, soil_moisture, light, nitrogen, phosphorus, potassium):
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )

        cursor = connection.cursor()
        insert_query = """
        INSERT INTO sensor_readings (temperature, humidity, soil_moisture1, soil_moisture2, soil_moisture3, soil_moisture4, soil_moisture5, soil_moisture6, light, nitrogen, phosphorus, potassium)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        record = (temperature, humidity, soil_moisture[0], soil_moisture[1], soil_moisture[2], soil_moisture[3], soil_moisture[4], soil_moisture[5], light, nitrogen, phosphorus, potassium)
        cursor.execute(insert_query, record)
        connection.commit()
        print("Record inserted successfully: ", record)

    except Error as error:
        print(f"Failed to insert record into MySQL table: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.data.decode('utf-8')
    if not data:
        return jsonify({'error': 'Invalid data format'}), 400

    # Append raw data to the in-memory list
    received_data.append(data)
    print("Received data:", data)

    try:
        # Extract data for MySQL insertion
        parts = data.split(', ')
        if len(parts) < 12:
            raise ValueError("Insufficient data received")

        temperature = float(parts[0].split(': ')[1].replace(' °C', ''))
        humidity = float(parts[1].split(': ')[1])
        light_str = parts[2].split(': ')[1].replace(' lux', '')
        light = float(light_str) if light_str != 'NAN' else 0
        nitrogen = int(parts[3].split(': ')[1].replace(' mg/kg', ''))
        phosphorus = int(parts[4].split(': ')[1].replace(' mg/kg', ''))
        potassium = int(parts[5].split(': ')[1].replace(' mg/kg', ''))

        # Extract soil moisture values
        soil_moisture = []
        for i in range(6):
            soil_moisture.append(int(parts[6 + i].split(': ')[1].replace('%', '')))

        # Insert data into MySQL
        insert_sensor_data(temperature, humidity, soil_moisture, light, nitrogen, phosphorus, potassium)
    except Exception as e:
        print(f"Error processing data: {e}")
        return jsonify({'error': 'Failed to process data'}), 500

    return jsonify({'status': 'success'}), 200

@app.route('/data', methods=['GET'])
def get_data():
    formatted_data = []
    for entry in received_data:
        entry = entry.replace(' °C', '').replace(' lux', '').replace(' mg/kg', '').replace('%', '')
        entry = entry.replace('Soil Moisture Values:', 'Soil Moisture')
        entry = entry.replace('Sensor ', 'Sensor')
        formatted_data.append(entry)
    
    return '<br>'.join(formatted_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
