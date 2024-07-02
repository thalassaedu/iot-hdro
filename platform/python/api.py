from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="192.168.2.177",  # Updated to match your MySQL server host
            port=30036,  # Specify the custom port here
            user="root",
            password="test1234",  # Replace with your MySQL root password
            database="sensor_data"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        else:
            print("Failed to connect to MySQL database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

@app.route('/update', methods=['POST'])
def update_sensor_data():
    try:
        temperature = request.form.get('temperature')
        humidity = request.form.get('humidity')
        soil_moisture = request.form.get('soilMoisture')

        connection = create_connection()
        if connection is None or not connection.is_connected():
            raise Exception("Failed to connect to the database")

        cursor = connection.cursor()

        query = """
        INSERT INTO sensor_readings (temperature, humidity, soil_moisture)
        VALUES (%s, %s, %s)
        """
        values = (temperature, humidity, soil_moisture)

        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
