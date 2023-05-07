setup.sh
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
    echo "CAMERA_DEVICE=$camera_device" > backend/.env
fi

# Build and run the Docker container
echo "Building Docker image"
sudo docker build -t camera-app --build-arg CAMERA_DEVICE=$CAMERA_DEVICE -f Dockerfile .

echo "Running Docker container"
sudo docker run --rm -it --device $camera_device:$camera_device -p 5000:5000 --env-file backend/.env camera-app
