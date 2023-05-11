# Live Video Streaming with USB Camera and Real-Time Object Detection and Facial Recognition

# Environment

* Linux
  * Ubuntu 22.04 LTS (Recommended)

# Prerequisites

Download and install the following software:

* [Python 3](https://www.python.org/downloads/)
* [Docker](https://docs.docker.com/engine/install/ubuntu/)

# Installation

Docker installation:

```shell
sudo apt-get update -y
sudo apt-get install ca-certificates curl gnupg -y

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

# Usage

## Setup

Give permission to the setup script:

```shell
chmod +x setup.sh
```

Run the following command to start the application:

```shell
./setup.sh
```

## Start the Application 

To start the application, run the following command:

```shell
sudo docker compose up --build
```

## Stop the Application

To stop the application, press `CTRL + C` and run the following command:

```shell
sudo docker compose down
```

# Credits

This project uses the following resources:

- [YOLOv8](https://github.com/ultralytics/ultralytics)
- [Node.js](https://nodejs.org/)
- [React App](https://create-react-app.dev/)
- [Flask](https://flask.palletsprojects.com/)
- [OpenCV](https://opencv.org/)
- [Docker](https://www.docker.com/)
- [Deepface](https://github.com/serengil/deepface)

# TODO

- [ ] When the browser refreshes, the `yolo_enabled` should be reset to `false`.
- [ ] Make the web interface look appealing and add more features.
