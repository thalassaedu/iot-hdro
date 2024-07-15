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
    data = request.json
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    soil_moisture = data.get('soilMoisture')
    light = data.get('light')
    nitrogen = data.get('nitrogen')
    phosphorus = data.get('phosphorus')
    potassium = data.get('potassium')

    if None in [temperature, humidity, soil_moisture, light, nitrogen, phosphorus, potassium]:
        return jsonify({'error': 'Invalid data'}), 400

    insert_sensor_data(temperature, humidity, soil_moisture, light, nitrogen, phosphorus, potassium)
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
