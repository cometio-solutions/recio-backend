#! /bin/bash

echo "Installing requirements..."
pip3 install -r requirements.txt > /dev/null
echo "Requirements installed."

exec "$@"