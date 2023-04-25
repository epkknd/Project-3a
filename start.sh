#!/bin/bash

# Start Redis
redis-server --daemonize yes

# Run the Python app
python api.py