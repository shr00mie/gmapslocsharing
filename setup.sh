#!/bin/bash
#
## -------------------------------=[ Info ]=--------------------------------- ##
#
## -=[ Author ]=------------------------------------------------------------- ##
#
# shr00mie
# 03.14.2019
# v0.2
#
## -=[ Use Case ]=----------------------------------------------------------- ##
#
# Appends google-chrome-stable install to base homeassistant Dockerfile.
#
## -=[ Breakdown ]=---------------------------------------------------------- ##
#
# 1. Create directories.
# 2. Clone custom component elements into build directory.
# 3. Copy custom_components and deps folders into HA mount (config) directory.
# 4. Generate custom Dockerfile to build directory.
# 5. Generate sample docker-compose.yaml file to base HA directory.
# 6. Set permissions on base HA directory.
# 7. Build custom image as hasschrome:latest
#
## -=[ To-Do ]=-------------------------------------------------------------- ##
#
# I'm sure a bunch...
#
## -=[ Requirements ]=------------------------------------------------------- ##

# 1. The following assumptions are being made:
#    - docker-ce and git are installed
#    - your user is a member of the docker group (sudo adduser $USER docker)

## -=[ Functions ]=---------------------------------------------------------- ##
#
# Usage: status "Status Text"
function status() {
  GREEN='\033[00;32m'
  RESTORE='\033[0m'
  echo -e "\n...${GREEN}$1${RESTORE}...\n"
}
#
## -----------------------------=[ Variables ]=------------------------------ ##

# grabs user ID
User_ID=$(id -u)
# grabs docker group ID
Docker_ID=$(cat /etc/group | grep docker | cut -d: -f3)
# location to base home assistant mount directory
HA_Base_Dir="/home/$USER/docker/hass"
HA_Build_Dir="$HA_Base_Dir/build"
HA_Mount_Dir="$HA_Base_Dir/config"

## ---------------------------=[ Script Start ]=----------------------------- ##

status "Creating directories"
mkdir -p $HA_Build_Dir
mkdir -p $HA_Mount_Dir

status "Cloning custom component into build directory"
git clone https://github.com/shr00mie/gmapslocsharing.git -b docker $HA_Build_Dir

status "Copying custom component into /config directory"
cd $HA_Build_Dir
cp -r custom_components deps ../config

status "Generating Dockerfile to: $HA_Build_Dir"
cat << EOF | tee $HA_Build_Dir/Dockerfile > /dev/null
FROM homeassistant/home-assistant:latest
LABEL maintainer="Say hello to your mother for me..."
ENV DEBIAN_FRONTEND="noninteractive"

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | \
    tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install apt-utils -y && \
    apt-get upgrade -y && \
    apt-get install \
    google-chrome-stable \
    git \
    python3-pip -y && \
    pip3 install -U pip setuptools wheel && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoclean && \
    apt-get autoremove -y && \
    chmod -R 774 /config
EOF

status "Generating docker-compose example to: $HA_Base_Dir"
cat << EOF | tee $HA_Base_Dir/docker-compose.yaml > /dev/null
version: 2
services:
  hasschrome:
    image: hasschrome:latest
    user: "$User_ID:$Docker_ID"
    container_name: hasschrome
    hostname: hasschrome
    restart: unless-stopped
    # domainname:
    network_mode: host
    # ports:
    # dns:
    volumes:
      - $HA_Mount_Dir:/config
      - /etc/localtime:/etc/localtime:ro
    environment:
      - PUID=$User_ID
      - GUID=$Docker_ID
    # labels:
    # devices:
EOF

status "Setting permissions on $HA_Mount_Dir"
chown -R "$USER:docker" $HA_Base_Dir
chmod -R g+w $HA_Base_Dir

status "Building custom image: hasschrome:latest (this could take a while)"
docker build --quiet --label hasschrome --tag hasschrome:latest $HA_Build_Dir &> /dev/null
