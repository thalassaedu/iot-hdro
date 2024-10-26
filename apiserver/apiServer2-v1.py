import pymysql
import time
from flask import Flask, jsonify
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

# MySQL database connection details
DB_HOST = '192.168.2.221'
DB_PORT = 30036
DB_USER = 'root'
DB_PASSWORD = 'test1234'
DB_NAME = 'sensor_data_db'

# Retry attempts for lock timeout errors
MAX_RETRIES = 3

# MySQL connection using SQLAlchemy
def get_db_connection():
    connection_string = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(connection_string)
    return engine

# Function to delete previous data for the current day
def delete_previous_data(date, cursor):
    # SQL delete statement to remove data for the current date
    delete_query = "DELETE FROM lux_range_data WHERE date = %s"
    cursor.execute(delete_query, (date,))

# Function to insert the calculated data into MySQL
def insert_lux_data_to_mysql(data):
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
            cursor = connection.cursor()

            # SQL insert statement for inserting the data
            insert_query = """
            INSERT INTO lux_range_data (date, lux_range_0_100, lux_range_101_500, lux_range_501_2000, lux_range_2001_7000, lux_range_7000_plus)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            # Begin transaction
            connection.begin()

            # Iterate through the data and insert row by row
            for date, lux_values in data.items():
                # Delete previous data for the current date within the transaction
                delete_previous_data(date, cursor)
                
                # Insert new calculated data
                cursor.execute(insert_query, (
                    date, 
                    lux_values.get('0-100', 0),
                    lux_values.get('101-500', 0),
                    lux_values.get('501-2000', 0),
                    lux_values.get('2001-7000', 0),
                    lux_values.get('7000+', 0)
                ))

            # Commit the transaction
            connection.commit()
            cursor.close()
            connection.close()
            print("Data inserted successfully")
            break  # Exit the retry loop if successful

        except pymysql.err.OperationalError as e:
            print(f"Error occurred: {e}")
            if "Lock wait timeout exceeded" in str(e):
                retry_count += 1
                print(f"Retrying... Attempt {retry_count}")
                time.sleep(2)  # Add a small delay before retrying
            else:
                # If the error is not related to lock timeout, re-raise it
                raise
        finally:
            if connection and connection.open:
                connection.rollback()  # Rollback transaction on failure

# Function to fetch, calculate, and insert LUX range data
def calculate_and_insert_lux_time():
    engine = get_db_connection()

    # Query to fetch timestamp and Lux columns
    query = "SELECT timestamp, Lux FROM sensor_data WHERE timestamp IS NOT NULL ORDER BY timestamp ASC"
    
    # Fetch the data from MySQL into a pandas DataFrame
    df = pd.read_sql(query, engine)

    # Debug: Check if data is fetched
    if df.empty:
        print("No data fetched from MySQL!")
        return {}

    # Convert timestamp and LUX to appropriate formats
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['Lux'] = pd.to_numeric(df['Lux'], errors='coerce')

    # Drop invalid rows
    df = df.dropna(subset=['timestamp', 'Lux'])

    # Calculate time differences between consecutive rows in hours
    df = df.sort_values(by='timestamp')
    df['time_diff'] = df['timestamp'].diff().dt.total_seconds() / 3600
    df['time_diff'] = df['time_diff'].fillna(0)

    # Define LUX ranges
    ranges = {
        '0-100': (0, 100),
        '101-500': (101, 500),
        '501-2000': (501, 2000),
        '2001-7000': (2001, 7000),
        '7000+': (7001, float('inf'))
    }

    # Initialize result dictionary
    result = {}
    df['date'] = df['timestamp'].dt.date

    # Process data day by day
    for day in df['date'].unique():
        day_data = df[df['date'] == day]
        result[str(day)] = {}

        for range_label, (low, high) in ranges.items():
            # Filter data for the given LUX range
            range_data = day_data[(day_data['Lux'] >= low) & (day_data['Lux'] <= high)]
            # Sum the time differences for this range
            total_time = range_data['time_diff'].sum()
            result[str(day)][range_label] = round(total_time, 2)

    # Insert the result into the lux_range_data table in MySQL
    insert_lux_data_to_mysql(result)

    return result

# API route to get and insert the LUX time range data
@app.route('/lux-time-ranges', methods=['GET'])
def get_lux_time_ranges():
    result = calculate_and_insert_lux_time()
    return jsonify(result)

# Start the Flask API
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)
