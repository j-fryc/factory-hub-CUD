#!/bin/sh
mkdir -p /app/data
# Run the API
cd /app
alembic upgrade head
fastapi run main.py --port 8200