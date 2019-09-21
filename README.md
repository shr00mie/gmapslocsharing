# gmapslocsharing
Definitely not a Home Assistant helper library designed to pretend to be a browser in order to grab location sharing GPS info instead of paying for the maps api...

# Why you do this?
Wasn't a huge fan of how locationsharinglib was working and processing information. Decided to see if I could conjure up a more consistent method.

# Contents
## Manual install or venv:
- custom_components folder: google_maps device_tracker component.
- deps folder: gmapslocsharing package
## Docker
- same as above
- setup.sh script to add chromium browser & driver binary layer to HA's alpine
along with entrypoint script to drop from root user to same UID:GID as local
os.
- sameple directory with standalone entrypoint and dockerfile contents.
- custom docker image name = hass-chrome:latest

# Dependencies
- 2FA via device sign-in prompt on google account.
- google-chrome-stable==77.0.3865.90
- chromedriver-binary==77.0.3865.40.0
- selenium==3.141.0
- selenium-wire==1.0.9
- geohash2==1.1

# Instructions
For the manual & venv installs, run the required scripts to install chrome/chromium
browser and chromedriver. make sure custom components and deps contents are located
in the appropriate destinations for your setup.

## HA Config
`debug`: I've included a ton of debugging in case the component starts going a bit wonky. If things start going tits up, set debug to true and it'll output all the URLs, take screenshots of the login process, and dump raw output and errors to a debug folder under the HA config directory.

```yaml
- platform: google_maps
  username: !secret google_maps_email
  password: !secret google_maps_pass
  debug: false
```

## Manual Linux Install
For the time being, there's just two scripts for manual linux installs.
- Ubuntu
- CentOS

Throw them in your home folder, modify the paths as necessary, `chmod u+x` on the
file and run. If you're on another OS, hit me up with a script for your use case
so it can be added below.

### Ubuntu:
```
#!/bin/bash

# modify this path as necessary to reflect your installation
HA_PATH="$HOME/.homeassistant"
TEMP="$HOME/gmaps_temp"

wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

cat << EOF | sudo tee /etc/apt/sources.list.d/google-chrome.list
deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main
EOF

sudo apt update && sudo apt install google-chrome-stable git -y

mkdir $TEMP
git clone https://github.com/shr00mie/gmapslocsharing.git $TEMP
cp -r $TEMP/custom_components $TEMP/deps $HA_PATH
rm -rf $TEMP
```
### Cent OS: (thanks, [lleone71](https://github.com/lleone71)!)
```
#!/bin/bash

# modify this path as necessary to reflect your installation
HA_PATH="$HOME/.homeassistant"
TEMP="$HOME/gmaps_temp"

cat << EOF | sudo tee /etc/yum.repos.d/google-chrome.repo
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
EOF

sudo yum install google-chrome-stable git -y

mkdir $TEMP
git clone https://github.com/shr00mie/gmapslocsharing.git $TEMP
cp -r $TEMP/custom_components $TEMP/deps $HA_PATH
rm -rf $TEMP
```
## Docker
- Builds the custom image with a label:tag of hass-chrome:latest.

Feel free to modify anything necessary to get this functional. I suspect this will
become considerably more streamlined when converted to a proper PiPy package.

# Updates
[ 09.03.2019]
- reconfigured gmapslocsharing for the new HA alpine image. setup.sh has been updated
with the necessary changes. using chromium-browser and chromium-chromedriver from alpine's
edge repo. should cut down or entirely eliminate browser and driver version mismatch.
not all args are available for chromium, so bear with me while i get the right mix going.

[ 08.15.2019]
- fell down a rabbit hole optimizing the Dockerfile for the modified HA+Chrome
image.
- introduced entrypoint which grabs requirements as root and then switches to a
predefined user:group to run the homeassistant as.
- pretty big refactor of setup.sh. should now be able to just throw that in a
script on your docker server, change some variables if necessary, and let it rip.
- should go without saying, but examine the contents and modify for your environment
as required.
- dropped country HA config option under device_tracker platform.
this will probably break shit, so if you were using it, check and
remove it from your config.
- updated the manual install scripts.

[ 08.12.2019 ]
- so...you know how sometimes you start replacing a light bulb and before you
know it you're under the car replacing the O2 sensor...that's basically what happened.
- entirely ripped out requests. replaced response body functionality via selenium-wire.
- introduced configparser for passing data between modules.
- NO MORE FUCKING COOKIE FILE. since we're using chrome, it's all in the chrome
data folder. welcome to the future.
- cleaned up raw response parsing.

[ 07.25.2019 ]
- the latest version of the chrome browser appears to be outputting decompressed
bytes instead of brotli compressed data. refactored and removed brotli dependency.
- while i was refactoring, think i managed to cover every edge case, so we
should always be seeing complete data without any errors...at least until they tweak
something.
- i've also added geohash computation for anyone who likes messing around with
grafana. right now it's defaulting to precision=12 for the granularity. as soon
as my fingers stop hurting, i'll probably come back and add precision as a config
option for anyone who needs it.

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

# Astrixe's and whatnot
I'd call this a solid beta at this point. I'm sure there are plenty of improvements
to be made. Be gentle. If something breaks, set debug to true, and hit me up with
the logs and contents from config/debug folder.

I highly recommend enabling 2FA via device notifications on the account with
which you are sharing individual locations. This allows for 2FA while not
requiring any input/interaction with the initiator. This should allow for
captcha bypass and seems like the best approach for this use case.

# ToDo:
- Figure out where things can go wrong. Catch said wrong things. Provide output
to user.
- Hass.io or HACAS implementation.

# And then?
If people like this, then I'm going to need a decent amount of help/input on how
to turn this into a proper package as this would be my first.
