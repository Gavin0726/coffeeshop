#!/usr/bin/env bash
# This file tags and uploads an image to Docker Hub

# Assumes that an image is built via `run_docker.sh`

# Step 1:
# Create dockerpath
dockerpath="lnguoxun/coffeeshopfrontend"

# Step 2:  
# Authenticate & tag
echo "Docker ID and Image: $dockerpath"
docker image tag coffeeshopfrontend:latest $dockerpath:coffeeshopfrontend_v2.3
docker login --username lnguoxun
# Step 3:
# Push image to a docker repository
docker push $dockerpath:coffeeshopfrontend_v2.3