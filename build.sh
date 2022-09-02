#!/bin/bash
cd /home/daniel/realsense_docker
pipreqs src/
docker build --tag realsense_docker .
