#!/bin/bash

# Use Heroku's PORT if it's set, otherwise use a default port for local development
PORT=${PORT:-8080}

# Start the FastAPI server with the appropriate port
uvicorn api:app --host 0.0.0.0 --port $PORT
