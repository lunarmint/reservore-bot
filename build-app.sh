#!/bin/bash

# Remove the previous instances.
docker container stop reservore-bot && docker container rm reservore-bot

# Build the project using docker-compose.
docker-compose pull

# Prune any dangling images.
docker image prune -f

# Prune any dangling volumes.
docker volume prune -f

# Start the containers.
docker-compose up -d
