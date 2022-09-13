FROM ubuntu:18.04

LABEL maintainer="dale@create.aau.dk"
LABEL version="0.1"
LABEL description="A custom Docker Image for running RealSense on Ubunt 22."

ARG  DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y gnupg2
RUN apt-get install -y lsb-release
RUN apt-get install -y software-properties-common
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
RUN add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" -u
RUN apt-get install -y python3-pip
RUN apt-get install -y qt5-default
RUN apt-get install -y librealsense2-dkms
RUN apt-get install -y librealsense2-utils
RUN apt-get install -y librealsense2-dev
RUN apt-get install -y librealsense2-dbg
RUN apt-get install -y nano
RUN apt-get install -y python3-tk.
RUN apt-get autoremove
RUN apt-get autoclean

ENV QT_X11_NO_MITSHM=1

WORKDIR /src
COPY src/requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
COPY src/main.py  main.py
COPY src/gui/server.py server.py
COPY src/gui/gui_client.py gui_client.py 
COPY src/gui/realsense_client.py realsense_client.py
COPY src/gui/launcher.sh launcher.sh
COPY src/check_height.py check_height.py
RUN chmod +x launcher.sh
#CMD [ "python3", "src/main.py"]
