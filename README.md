# iot-hdro
This is Hydroponic IOT repository.

1. The entire solution is based on RKE k8 cluster. 
2. To access cluster :
    - kube-rke on my mac machine.
    - Cluster is running on 3 nodes : 192.168.2.177, 178,179.
    - To access RKE rancher - "/rancher.dockr.life/"
        username - admin
        password - bootStrapAllTheThings

        - For more rancher or k8 cluster troubleshooting :
            - /Users/D073341/work/sre-cops/thaedu-course --> under k8
3. Initial Python is running on lab-server : 
        3. Server : 192.168.2.162 - System-lab
            a. Lab6/Abcd1234
                Root/Linux5000

4.  venv
    - python3 -m venv venv
    - Activate Virtual Environment
        source venv/bin/activate
    - Install Dependencies
        pip3 install -r requirements.txt
    - Deactivated
        deactivate
    - pip3 install flask mysql-connector-python



# Need to create solution that will read soil moisture, environment temprature and humidity and send it to database. database will be connected via grafana
    - As this entire solution will be build on kubernetes.
    

## Applications
    - Mysql
        - Under mysql folder
        - First create a pv using longhorn with name of "mysql-iot-pv".
        - Create "mysql-iot-pvc" using pv.
        - update ovc information inside mysql deployment. 
        - Create secret.
        - Create deployment
        - Create service - it is using node IP.
    - Mysql connection:
        - Use node IP : 192.168.2.177 over port 30036 - database mysql - user root/Abcd1234

## Running sessoin on background: 
    115096.mysession
    - screen -S mysession
    - Press Ctrl+A, then D. This will detach the session and keep your script running in the background.

        Disconnect from SSH:

        Simply log out or close the terminal.

        
