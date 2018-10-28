# gmapslocsharing
Definitely not a Home Assistant helper library designed to pretend to be a browser in order to grab location sharing GPS info instead of paying for the maps api...

# Why you do this?
Wasn't a huge fan of how locationsharinglib was working and processing information. Decided to see if I could conjure up a more consistent method.

# Contents
- custom_components folder: contains proposed modifications to google_maps device_tracker component.
- deps folder: proposed new google maps location sharing package.

# Dependencies
- selenium==3.14.1 or latest
- chromedriver-binary==2.42.0 or latest
- brotli==1.0.6 or latest
- requests==2.20.0
- google-chrome


For google chrome ubuntu console install, throw the below into a .sh and run.
modify as necessary for other environments:

```
#!/bin/bash
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
cat << EOF | sudo tee /etc/apt/sources.list.d/google-chrome.list
deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main
EOF
sudo apt update && sudo apt install google-chrome-stable -y
```

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
- figure out where things can go wrong. catch said wrong things. provide output
to user.
- test and add scenarios for alternative login methods. example would be
something like adding dashboard pop-up if using google authenticator and have
input be passed from UI to selenium for login.
- localization module has been added. if i get some time, i'll use a vpn to
start going through the login process for other countries. if you see that the
localization dict does not contain the entries for your country, feel free to
compose and add a PR.

# And then?
If people like this, then I'm going to need a decent amount of help/input on how
to turn this into a proper package as this would be my first.
