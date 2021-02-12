#!/bin/bash

docker image rm russboshep/react-nginx-test-kube:latest
docker build -t russboshep/react-nginx-test-kube:latest .
docker push russboshep/react-nginx-test-kube:latest