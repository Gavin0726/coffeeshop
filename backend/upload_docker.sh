#!/usr/bin/env bash
# This file tags and uploads an image to Docker Hub

# Assumes that an image is built via `run_docker.sh`

# Step 1:
# Create dockerpath
dockerpath="lnguoxun/coffeeshopbackend"

# Step 2:  
# Authenticate & tag
echo "Docker ID and Image: $dockerpath"
docker image tag coffeeshopbackend:latest $dockerpath:coffeeshopbackend_v1.1
docker login --username lnguoxun
# Step 3:
# Push image to a docker repository
docker push $dockerpath:coffeeshopbackend_v1.1