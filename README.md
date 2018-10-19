# gmapslocsharing
Definitely not a library designed to pretend to be a browser in order to grab location sharing GPS info instead of paying for the maps api...

# Why you do this?
Wasn't a huge fan of how locationsharinglib was working and processing information. Decided to see if I could conjure up a more consistent method.

# Contents
- custom_components folder: contains proposed modifications to google_maps device_tracker component.
- deps folder: proposed new google maps sharing library.

# Dependencies
- selenium==3.14.1 or latest
- chromedriver-binary==2.42.0 or latest
- brotli==1.0.6 or latest
- google-chrome

For google chrome console install, throw the below into a .sh and run:

```
#!/bin/bash
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
cat << EOF | sudo tee /etc/apt/sources.list.d/google-chrome.list
deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main
EOF
sudo apt update && sudo apt install google-chrome-stable -y
```

# Now what
For the time being, the repo is designed in such a way that you should be able to clone it from the .homeassistant folder and it should put the google_maps and package
in their proper respective locations a la something like:

`git clone https://github.com/shr00mie/gmapslocsharing.git <path_to_.homeassistant>`
