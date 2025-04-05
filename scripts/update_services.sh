#!/usr/bin/env bash
set -x  # Print each command before running

# Save any uncommitted changes
git stash

# Replace "dev" with "pro" in config (switch environment to production mode)
sed -i 's/dev/pro/g' ./config/global_config.toml

# Pull the latest code
git pull

# Rebuild and restart the services using Docker Compose
docker-compose up -d --build

# Remove any dangling Docker images with <none> tag
docker images | grep "<none>" | awk '{print $3}' | xargs -r docker rmi -f

# Tail logs from Docker services (last 1000 lines)
docker-compose logs -f --tail 1000
