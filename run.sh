#!/bin/bash
xhost +local:docker
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
docker run -it --rm --privileged -e DISPLAY=$DISPLAY -v $XSOCK:$XSOCK -v $XAUTH:$XAUTH -e XAUTHORITY=$XAUTH realsense_docker
xhost -local:docker
