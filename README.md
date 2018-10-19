# gmapslocsharing
Definitely not a library designed to pretend to be a browser in order to grab location sharing GPS info instead of paying for the maps api...

# why you do this?
Wasn't a huge fan of how locationsharinglib was working and processing information. Decided to see if I could conjure up a more consistent method.

# contents
custom_components folder: contains proposed modifications to google_maps device_tracker component.
deps folder: proposed new google maps sharing library.

# dependencies
selenium==3.14.1 or latest
chromedriver-binary==2.42.0 or latest
google-chrome

# now what
for the time being, the repo is designed in such a way that you should be able to clone it from the .homeassistant folder and it should put the google_maps and package
in their proper respective locations.
