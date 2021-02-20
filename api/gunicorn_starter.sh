#!/bin/sh

# Change directory to /app/api, run server.py/app function
gunicorn --chdir /app/api server:APP -w 2 --threads 2 -b 0.0.0.0:8000 --access-logfile accesslog.txt --capture-output --log-level debug --error-logfile errors.txt