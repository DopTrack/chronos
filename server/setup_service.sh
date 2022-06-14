#!/bin/bash

SERVICE_FILE=webappservercontrol
PYTHON_LOG=pythonDoptrackServer
NAME=doptrackwebappserver
USERNAME=root

echo "Copying files..."
cp -v "init.d/$SERVICE_FILE" "/etc/init.d/$NAME"
chmod +x "/etc/init.d/$NAME"

mkdir /opt/doptrackwebappserver/
cp -v services/* /opt/doptrackwebappserver/

echo "Creating log files..."
touch "/var/log/$NAME.log" && chown "$USERNAME" "/var/log/$NAME.log"
touch "/var/log/$PYTHON_LOG.log" && chown "$USERNAME" "/var/log/$PYTHON_LOG.log"

# Starting service
update-rc.d "$NAME" defaults
service "$NAME" start