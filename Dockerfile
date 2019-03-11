FROM homeassistant/home-assistant:latest
MAINTAINER Jim Shank <jshank@theshanks.net>

RUN set -x && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
      && printf "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
      && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
      google-chrome-stable \
      && rm -rf /var/lib/apt/lists/*
