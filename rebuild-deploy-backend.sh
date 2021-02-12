#!/bin/bash

cd api
docker image rm russboshep/flask-gunicorn-test:latest
docker build -t russboshep/flask-gunicorn-test:latest .
docker push russboshep/flask-gunicorn-test:latest