FROM homeassistant/home-assistant:latest
LABEL maintainer="Jim Shank <jshank@theshanks.net>"
ENV DEBIAN_FRONTEND="noninteractive"

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | \
    tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y \
    google-chrome-stable \
    git && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoclean && \
    apt-get autoremove -y && \
    chmod -R 774 /config
