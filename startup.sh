#!/bin/bash

# Force release of audio devices, fixes "Device or resource busy" error on amplifier
sudo fuser -k /dev/snd/*

# Set the base directory to the location of this script
BASE_DIR="$(dirname "$(realpath "$0")")"

# Ensure any existing instance of main.py is terminated
sudo pkill -f "$BASE_DIR/main.py"

# Start necessary services
# sudo modprobe bcm2835-v4l2 # Enable camera (if needed)
sudo pigpiod # Start the GPIO daemon.



# Accept an optional environment argument and pass as --env (default to no argument, main.py defaults to 'robot')
if [ -n "$1" ]; then
	ENV_ARG="--env $1"
else
	ENV_ARG=""
fi
"$BASE_DIR/myenv/bin/python3" "$BASE_DIR/main.py" $ENV_ARG

# start mosquitto for mqtt broker
# sudo systemctl start mosquitto