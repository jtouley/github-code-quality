#!/bin/bash

echo "Setting up the Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install -r config/requirements.txt

echo "Installing linting tools (black, flake8)..."
pip install black flake8

echo "Exporting PYTHONPATH to include 'src/' for pytest..."
export PYTHONPATH=$(pwd)/src
echo "PYTHONPATH set to: $PYTHONPATH"

echo "Setup complete. Run 'source venv/bin/activate' to start coding!"
echo "Run 'pytest tests/' to execute tests."