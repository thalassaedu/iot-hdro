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
        record = (soil_moisture1, soil_moisture2, soil_moisture3, soil_moisture4, soil_moisture5
