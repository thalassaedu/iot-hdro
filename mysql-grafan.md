# Mysql information
    - Mysql server : 192.168.2.221:30036
        - User: root
        - Pass: Test1234
        - DB: sensor_data_db
            - table: sensor_data
                - Fields : timestamp, N, P, K, Temperature, Humidity, LUX
        
# Grafana Mysql queries
    - Capture the NPK values : 
        SELECT
        timestamp AS "time",
        N AS "Nitrogen",
        P AS "Phosphorus",
        K AS "Potassium"
        FROM
        sensor_data
        ORDER BY
        timestamp ASC;
        