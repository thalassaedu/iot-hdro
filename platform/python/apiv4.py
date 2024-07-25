from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

MYSQL_HOST = '192.168.2.194'
MYSQL_PORT = 30036
MYSQL_DATABASE = 'sensor_data'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'test1234'

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
        INSERT INTO sensor_readings (temperature, humidity, soil_moisture, light, nitrogen, phosphorus, potassium)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        record = (temperature, humidity, soil_moisture, light, nitrogen, phosphorus, potassium)
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

@app.route('/update', methods=['POST'])
def update():
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'Invalid data format'}), 400

    try:
        # Log the raw data received
        print("Received data:", data)
        
        # Parsing the data string
        parts = data.split(', ')
        
        # Ensure there are enough parts to parse
        if len(parts) < 12:
            print("Not enough parts in data:", len(parts))
            return jsonify({'error': 'Not enough data parts received'}), 400
        
        # Extract and log individual parts
        print("Data parts:", parts)
        
        soil_moisture = ', '.join(parts[:6])
        print("Soil Moisture:", soil_moisture)
        
        temperature = float(parts[6].split(': ')[1].split(' ')[0])
        humidity = float(parts[7].split(': ')[1].split(' ')[0])
        light = float(parts[8].split(': ')[1].split(' ')[0])
        nitrogen = int(parts[9].split(': ')[1].split(' ')[0])
        phosphorus = int(parts[10].split(': ')[1].split(' ')[0])
        potassium = int(parts[11].split(': ')[1].split(' ')[0])

        insert_sensor_data(temperature, humidity, soil_moisture, light, nitrogen, phosphorus, potassium)
        return jsonify({'status': 'success'}), 200
    except (IndexError, ValueError) as e:
        print("Error parsing data:", e)
        return jsonify({'error': f'Failed to parse data: {e}'}), 400

@app.route('/data', methods=['GET'])
def get_data():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sensor_readings")
        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'timestamp': row[1],
                'temperature': row[2],
                'humidity': row[3],
                'soil_moisture': row[4],
                'light': row[5],
                'nitrogen': row[6],
                'phosphorus': row[7],
                'potassium': row[8]
            })
        return jsonify(result)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
