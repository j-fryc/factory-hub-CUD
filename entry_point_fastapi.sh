#!/bin/bash
mkdir -p /app/data
# Run the API
fastapi run app/main.py --port 8200