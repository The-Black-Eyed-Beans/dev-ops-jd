#!/bin/bash

# create namespaces
kubectl apply -f ./namespace

# configure and deploy mysql
kubectl apply -f ./env/mysql-secret.yaml -f ./volume/mysql-pvc.yaml -f ./deployment/mysql-deployment.yaml -f ./service/mysql-service.yaml -f ./network-policy/mysql-policy.yaml -n aline-dev-mysql

# configure and deploy gateway
kubectl apply -f ./env/gateway-config.yaml -f ./deployment/gateway-deployment.yaml -f ./service/gateway-service.yaml -n aline-dev-gateway

echo "Sleeping $1 seconds before creating backend..."
sleep $1
# configure and deploy backend
kubectl apply -f ./env/backend -f ./env/mysql-secret.yaml -f ./deployment/backend/ -f ./service/backend-service.yaml -f ./network-policy/backend-policy.yaml -n aline-dev-backend