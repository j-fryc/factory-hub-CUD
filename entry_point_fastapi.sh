#!/bin/sh
mkdir -p /app/data
# Run the API
#cd /app
alembic -c /app/alembic.ini upgrade head
fastapi run app/main.py --port 8200