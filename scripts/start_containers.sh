#!/bin/bash

set -e

echo "Docker pull starting"

sudo docker pull yswork/music-customer-churn-prediction-ml:aws_prod_v1

echo "Docker image yswork/agriculture-yield-prediction-ml:aws_prod_v1 pulled successfully"

echo "Docker Run Starting on Port 7002"

sudo docker run -d -p 7002:7002 yswork/agriculture-yield-prediction-ml:aws_prod_v1

echo "Docker Run Successfully Started on Port 7002"