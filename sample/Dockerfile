FROM homeassistant/home-assistant:latest
LABEL maintainer="shr00mie"

ENV DEBIAN_FRONTEND="noninteractive"

COPY docker-entrypoint.sh /usr/src/app

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | \
    tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install apt-utils -y && \
    apt-get upgrade -y && \
    apt-get install \
    acl \
    google-chrome-stable \
    gosu \
    python3-pip -y && \
    pip3 install -U pip setuptools wheel && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoclean && \
    apt-get autoremove -y

RUN addgroup --gid $(cat /etc/group | grep docker | cut -d: -f3) docker && \
    adduser --system --uid $(id -u) --ingroup docker --disabled-login $USER

RUN chmod -R 770 /usr/src/app && \
    chmod +x docker-entrypoint.sh && \
    chown -R $USER:docker /config /home/$USER

RUN setfacl -R -m d:u:$USER:rwx,d:g:$docker:rwx,d:o::--- /config && \
    setfacl -R -m d:u:$USER:rwx,d:g:$docker:rwx,d:o::--- /home/$USER

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
CMD ["python","-m","homeassistant","-c","/config"]
