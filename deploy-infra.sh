#!/bin/bash

kubectl apply -f ./artshare-deployment.yml
kubectl apply -f ./artshare-service.yml
kubectl apply -f ./artshare-ingress.yml