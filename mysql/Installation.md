# MySQL Deployment on Kubernetes : https://phoenixnap.com/kb/kubernetes-mysql
    To successfully deploy a MySQL instance on Kubernetes, create a series of YAML files that you will use to define the following Kubernetes objects:

    A Kubernetes secret for storing the database password.
    A Persistent Volume (PV) to allocate storage space for the database.
    A Persistent Volume Claim (PVC) that will claim the PV for the deployment .
    The deployment itself.
    The Kubernetes Service.

## Step 1: Create Kubernetes Secret
## Step 2: Create Persistent Volume and Volume Claim
## Step 3: Create MySQL Deployment
## Access Your MySQL Instance
```bash
kubectl exec --stdin --tty mysql-694d95668d-w7lv5 -- /bin/bash
mysql -p
```

However, bear in mind the following two limitations:

This particular deployment is for single-instance MySQL deployment. It means that the deployment cannot be scaled - it works on exactly one Pod.
This deployment does not support rolling updates. Therefore, the spec.strategy.type must always be set to Recreate.

## Port forwared -
    - Login to log-700
    - su - rke
    - kubectl port-forward service/mysql 3306:3306 --address='0.0.0.0' &

