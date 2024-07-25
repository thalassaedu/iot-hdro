from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

MYSQL_HOST = '192.168.2.194'
MYSQL_PORT = 30036
MYSQL_DATABASE = 'sensor_data'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'test1234'

def insert_arduino_data(temperature, humidity, light, nitrogen, phosphorus, potassium):
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
        INSERT INTO arduino_data (temperature, humidity, light, nitrogen, phosphorus, potassium)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        record = (temperature, humidity, light, nitrogen, phosphorus, potassium)
        cursor.execute(insert_query, record)
        connection.commit()
        print("Arduino record inserted successfully: ", record)

    except Error as error:
        print(f"Failed to insert record into MySQL table: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def insert_esp32_data(soil_moisture1, soil_moisture2, soil_moisture3, soil_moisture4, soil_moisture5, soil_moisture6):
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
        INSERT INTO esp32_data (soil_moisture1, soil_moisture2, soil_moisture3, soil_moisture4, soil_moisture5, soil_moisture6)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        record = (soil_moisture1, soil_moisture2, soil_moisture3, soil_moisture4, soil_moisture5, soil_moisture6)
        cursor.execute(insert_query, record)
        connection.commit()
        print("ESP32 record inserted successfully: ", record)

    except Error as error:
        print(f"Failed to insert record into MySQL table: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/update_arduino', methods=['POST'])
def update_arduino():
    data = request.json
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    light = data.get('light')
    nitrogen = data.get('nitrogen')
    phosphorus = data.get('phosphorus')
    potassium = data.get('potassium')

    if None in [temperature, humidity, light, nitrogen, phosphorus, potassium]:
        return jsonify({'error': 'Invalid data'}), 400

    insert_arduino_data(temperature, humidity, light, nitrogen, phosphorus, potassium)
    return jsonify({'status': 'success'}), 200

@app.route('/update_esp32', methods=['POST'])
def update_esp32():
    data = request.json
    soil_moisture1 = data.get('soil_moisture1')
    soil_moisture2 = data.get('soil_moisture2')
    soil_moisture3 = data.get('soil_moisture3')
    soil_moisture4 = data.get('soil_moisture4')
    soil_moisture5 = data.get('soil_moisture5')
    soil_moisture6 = data.get('soil_moisture6')

    if None in [soil_moisture1, soil_moisture2, soil_moisture3, soil_moisture4, soil_moisture5, soil_moisture6]:
        return jsonify({'error': 'Invalid data'}), 400

    insert_esp32_data(soil_moisture1, soil_moisture2, soil_moisture3, soil_moisture4, soil_moisture5, soil_moisture6)
    return jsonify({'status': 'success'}), 200

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
        
        # Fetch data from arduino_data table
        cursor.execute("SELECT * FROM arduino_data")
        arduino_rows = cursor.fetchall()
        arduino_data = []
        for row in arduino_rows:
            arduino_data.append({
                'id': row[0],
                'timestamp': row[1],
                'temperature': row[2],
                'humidity': row[3],
                'light': row[4],
                'nitrogen': row[5],
                'phosphorus': row[6],
                'potassium': row[7]
            })
        
        # Fetch data from esp32_data table
        cursor.execute("SELECT * FROM esp32_data")
        esp32_rows = cursor.fetchall()
        esp32_data = []
        for row in esp32_rows:
            esp32_data.append({
                'id': row[0],
                'timestamp': row[1],
                'soil_moisture1': row[2],
                'soil_moisture2': row[3],
                'soil_moisture3': row[4],
                'soil_moisture4': row[5],
                'soil_moisture5': row[6],
                'soil_moisture6': row[7]
            })
        
        return jsonify({
            'arduino_data': arduino_data,
            'esp32_data': esp32_data
        })
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
