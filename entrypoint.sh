#! /bin/bash

echo "Updating pip..."
pip3 install --upgrade pip
echo "Pip updated."
echo "Installing requirements..."
pip3 install -r requirements.txt 
echo "Requirements installed."

exec "$@"
