#!/bin/sh

python3 server.py &
python3 gui_client.py &
python3 realsense_client.py