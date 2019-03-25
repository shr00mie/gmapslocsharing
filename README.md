# gmapslocsharing
Definitely not a Home Assistant helper library designed to pretend to be a browser in order to grab location sharing GPS info instead of paying for the maps api...

# Why you do this?
Wasn't a huge fan of how locationsharinglib was working and processing information. Decided to see if I could conjure up a more consistent method.

# Contents
- custom_components folder: contains proposed modifications to google_maps device_tracker component.
- deps folder: proposed new google maps location sharing package.

# Dependencies
- selenium==3.141.0
- chromedriver-binary==73.0.3683.68
- brotli==1.0.7
- requests==2.21.0
- google-chrome-stable

# Updates
[ 03.11.2019 ]
- [jshank](https://github.com/jshank) was kind enough to be my guinea pig over the
the weekend and get this package working with the docker HA install variant.
The docker components can be found under the docker branch. That branch includes
a Dockerfile and docker-compose template. The Dockerfile uses the existing HA
Dockerfile and appends the necessary code to facilitate the google-chrome-stable
install within the container. The docker-compose example is there for you to modify
as necessary for your use case.
- During the above adventure, a lot of...shortcomings?...were brought to light resulting
in a rather comprehensive rebuild of large parts of the package.
- In the not too distant future, I'd like to see about making this into a proper package
such that it can be installed within any docker variant via pip and maybe PR this
component over the existing and constantly breaking implementation within HA.

# Instructions
The store currently has two products to choose from. Ice cream and a magical box (Linux and Docker). We'll do our best to provide comprehensive instructions on how to get this component working with all documented configurations.

If something is unclear, incomplete, or does not work, let me know.

## Linux
As far as Linux flavors, we currently have Ubuntu and CentOS.

Should be able to throw the below into a .sh in your home folder, `chmod u+x` the script, and run with `./filename.sh`. If your HA config path is different from the one provided in the below
scripts, modify as necessary.

### Ubuntu:
```
#!/bin/bash

HA_PATH="/home/$USER/.homeassistant"

wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

cat << EOF | sudo tee /etc/apt/sources.list.d/google-chrome.list
deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main
EOF

sudo apt update && sudo apt install google-chrome-stable git -y

git clone https://github.com/shr00mie/gmapslocsharing.git $HA_PATH
```
### Cent OS: (thanks, [lleone71](https://github.com/lleone71)!)
```
#!/bin/bash

HA_PATH="/home/$USER/.homeassistant"

cat << EOF | sudo tee /etc/yum.repos.d/google-chrome.repo
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
EOF

sudo yum install google-chrome-stable git -y

git clone https://github.com/shr00mie/gmapslocsharing.git $HA_PATH
```
## Docker
At the moment, I've cobbled together a script which:
- Create build and config directories.
- Clone custom component docker branch into build directory.
- Copy custom_components and deps from build to config directory.
- Generates a Dockerfile which is basically just the stock homeassistant image with an appended google-chrome-stable install.
- Generates a sample docker-compose.yaml file with the custom entry.
- Sets permissions on the directory to be mounted into the HA container.
- Builds the custom image with a label:tag of hasschrome:latest.

Feel free to modify anything necessary to get this functional. I suspect this will
become considerably more streamlined when converted to a proper PiPy package.

# Now what
For the time being, the repo is designed in such a way that you should be able
to clone it directly into the .homeassistant folder and it should put the google_maps
and package in their proper respective locations a la something like:

`git clone https://github.com/shr00mie/gmapslocsharing.git <path_to_.homeassistant>`

# Astrixe's and whatnot
Be gentle. This should be considered development/proof of concept at best. I'm
sure there's a ton of pep8 crap I'm missing along with error checking and/or just
plain new programmer crap.

This solution would be considerably easier to implement in a containerized
variant of HomeAssistant as Chrome could be added to the build without requiring
any additional actions or input from the user to make this function. Users who
are installing HomeAssistant the custom/advanced method would have to run a
script to install.

I highly recommend enabling 2FA via device notifications on the account with
which you are sharing individual locations. This allows for 2FA while not
requiring any input/interaction with the initiator. This should allow for
captcha bypass and seems like the best approach for this use case.

# ToDo:
- Figure out where things can go wrong. Catch said wrong things. Provide output
to user.
- Test and add scenarios for alternative login methods. Example would be
something like adding dashboard pop-up if using Google authenticator and have
input be passed from UI to selenium for login.
- Localization module has been added. If I get some time, I'll use a VPN to
start going through the login process for other countries. If you see that the
localization dict does not contain the entries for your country, feel free to
compose and add a PR.

# And then?
If people like this, then I'm going to need a decent amount of help/input on how
to turn this into a proper package as this would be my first.
