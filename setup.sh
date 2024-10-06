#!/bin/bash

# This file is used to create a virtual environment for the project and install the dependencies
# It is recommended to use the venv module for this, but it is not always available

# Create a virtual environment if it doesn't already exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
