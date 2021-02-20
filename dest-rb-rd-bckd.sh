#!/bin/bash

./destroy-infra.sh
./rebuild-deploy-backend.sh
./deploy-infra.sh