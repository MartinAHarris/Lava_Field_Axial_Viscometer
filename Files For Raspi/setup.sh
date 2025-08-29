#!/usr/bin/env bash

# Make rc.local executable to enable all commands listed in there to run after
# automatically boot.
sudo chmod +x /etc/rc.local

# Install required packages
sudo apt-get update
sudo apt install python3-rpi.gpio

# If things install without problems, register penetrometer in rc.local
# Get the current working directory
INSTALLDIR="/opt/lava_field_penetrometer"
# Path to the code that needs to run at startup
PENFILE="Penetrometer_execution_code.py"

sudo mkdir -p "${INSTALLDIR}"                   #
sudo cp $PENFILE "${INSTALLDIR}/${PENFILE}"     # copy recorder file to install folder
# register recorder file for autostart
sudo python3 register_recorder.py "${INSTALLDIR}/${PENFILE}"