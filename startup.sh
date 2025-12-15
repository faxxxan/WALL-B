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


# Accept an optional environment argument (default to 'robot')
ENV_ARG="${1:-robot}"

# Run main.py using the virtual environment's Python interpreter, passing the environment argument
"$BASE_DIR/myenv/bin/python3" "$BASE_DIR/main.py" "$ENV_ARG"

# start mosquitto for mqtt broker
# sudo systemctl start mosquitto