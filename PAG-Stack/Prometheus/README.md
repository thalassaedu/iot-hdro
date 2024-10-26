## ☸️ kubernetes prometheus Setup

Complete prometheus monitoring stack setup on Kubernetes.

Idea of this repo to understand all the components involved in prometheus setup.

You can find the full tutorial from here--> [Kubernetes Monitoring setup Using Prometheus](https://devopscube.com/setup-prometheus-monitoring-on-kubernetes/)

## 🚀 CKA, CKAD, CKS, KCNA & PCA Coupon Codes

If you are preparing for CKA, CKAD, CKS, or KCNA exam, **save 20%** today using code **SCRIPT20** at https://kube.promo/devops. It is a limited-time offer. 

## Other Manifest repos

Kube State metrics manifests: https://github.com/devopscube/kube-state-metrics-configs

Alert manager Manifests: https://github.com/bibinwilson/kubernetes-alert-manager

Grafana manifests: https://github.com/bibinwilson/kubernetes-grafana

Node Exporter manifests: https://github.com/bibinwilson/kubernetes-node-exporter


## Deployment : Promotheus : https://phoenixnap.com/kb/prometheus-kubernetes
    kubectl create namespace monitoring
    k apply -f /Users/D073341/work/LaMa/gitrepo/argodep/PAG-Stack/Prometheus/clusterRole.yaml
    k apply -f /Users/D073341/work/LaMa/gitrepo/argodep/PAG-Stack/Prometheus/config-map.yaml
    k apply -f /Users/D073341/work/LaMa/gitrepo/argodep/PAG-Stack/Prometheus/prometheus-deployment.yaml
    k apply -f /Users/D073341/work/LaMa/gitrepo/argodep/PAG-Stack/Prometheus/prometheus-service.yaml

    kubectl port-forward  prometheus-deployment-84f65c89c5-prltw 8080:9090 -n monitoring


    To get the scrap metrics from the hosts: the hostn entry should be there into the prometheus "2-config-map.yaml". 
        scrape_configs:
      - job_name: 'HAC-node-exporter'
        static_configs:
          - targets: ['acvml2600:9100', 'acvml2601:9100', 'acvml2602:9100', 'acvml2603:9100', 'acvml2604:9100', 'acvml2605:9100', 'lvmql264:9100']

## Alert Manager
    7130  k apply -f /Users/D073341/work/LaMa/gitrepo/argodep/PAG-Stack/AlertManager/AlertManagerConfigmap.yaml
 7131  k apply -f /Users/D073341/work/LaMa/gitrepo/argodep/PAG-Stack/AlertManager/AlertTemplateConfigMap.yaml
 7132  k apply -f /Users/D073341/work/LaMa/gitrepo/argodep/PAG-Stack/AlertManager/Deployment.yaml
 7133  k get pods -n monitoring 
 7134  k apply -f /Users/D073341/work/LaMa/gitrepo/argodep/PAG-Stack/AlertManager/Service.yaml 
 7135  k get svc -n monitoring 
 7136  cd ..
 7137  git clone https://github.com/bibinwilson/kubernetes-grafana.git
 7138  ll
 7139  cd kubernetes-grafana
 7140  cp * /Users/D073341/work/LaMa/gitrepo/argodep/PAG-Stack/Grafana
 7141  k apply -f /Users/D073341/work/LaMa/gitrepo/argodep/PAG-Stack/Grafana/grafana-datasource-config.yaml
 7142  k apply -f /Users/D073341/work/LaMa/gitrepo/argodep/PAG-Stack/Grafana/deployment.yaml
 7143  k apply -f /Users/D073341/work/LaMa/gitrepo/argodep/PAG-Stack/Grafana/service.yaml


## Node exporter

    570  2023-09-06 15:55:22 cd /tmp/prommedia/
  571  2023-09-06 15:55:24 ls -lrt
  572  2023-09-06 15:55:30 tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz
  573  2023-09-06 15:55:32 cd node_exporter-1.6.1.linux-amd64/
  574  2023-09-06 15:55:36 ./node_exporter &


 ## Grafana











