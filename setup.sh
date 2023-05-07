#!/bin/bash
set -e

# Update the system
sudo apt-get update

# Install necessary dependencies
sudo apt-get install -y v4l-utils python3 python3-pip

# Install Python dependencies
pip3 install -r backend/requirements.txt

# Detect the camera device and write it to the .env file
camera_device=$(v4l2-ctl --list-devices 2>/dev/null | grep -Eo "/dev/video[0-9]+" | head -1)
if [ -z "$camera_device" ]; then
    echo "No camera device found."
    exit 1
else
    echo "Using camera device: $camera_device"
    echo "VIDEO_DEVICE=$camera_device" > .env
fi

# Export the VIDEO_DEVICE environment variable
export $(cat .env | xargs)

# Build and run the Docker container
echo "Building Docker image"
sudo docker build -t camera-app -f backend/Dockerfile .

echo "Running Docker container"
sudo docker compose up --build
