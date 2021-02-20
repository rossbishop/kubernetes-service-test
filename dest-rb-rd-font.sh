#!/bin/bash

./destroy-infra.sh
./rebuild-deploy-frontend.sh
./deploy-infra.sh