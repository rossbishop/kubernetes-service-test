#!/bin/bash

kubectl delete -f ./artshare-ingress.yml
kubectl delete -f ./artshare-service.yml
kubectl delete -f ./artshare-deployment.yml