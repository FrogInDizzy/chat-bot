#!/usr/bin/env bash
set -x  # Show log command being run

# Show real-time logs from Docker Compose (last 1000 lines)
docker-compose logs -f --tail 1000
