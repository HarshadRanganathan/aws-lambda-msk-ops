#!/bin/bash

# Publish the image to ECR registry
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin xxxxxxxxxx.dkr.ecr.us-east-1.amazonaws.com

docker tag kafka-ops-lambda xxxxxxxxxx.dkr.ecr.us-east-1.amazonaws.com/kafka-ops-lambda:latest

docker push xxxxxxxxxx.dkr.ecr.us-east-1.amazonaws.com/kafka-ops-lambda:latest
