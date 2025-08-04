#!/bin/bash

# Build and push Docker image to DockerHub

echo "Building Docker image..."
docker build -t sasuke1uchiha1ninja/example_repo:latest .

echo "Pushing Docker image to DockerHub..."
docker push sasuke1uchiha1ninja/example_repo:latest

echo "Docker image has been built and pushed successfully!"
echo "You can now run: docker-compose up -d"