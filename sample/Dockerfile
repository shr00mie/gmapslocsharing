FROM homeassistant/home-assistant:latest
LABEL maintainer="shr00mie"

COPY docker-entrypoint.sh /usr/src/app/docker-entrypoint.sh

RUN apk update && apk upgrade && \
    echo @edge http://nl.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories && \
    echo @edge http://nl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories && \
    echo @edge http://nl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories && \
    apk add --no-cache \
      python3@edge \
      python3-dev@edge \
      acl@edge \
      gosu@edge \
      chromium@edge \
      chromium-chromedriver@edge \
      nss@edge \
      freetype@edge \
      freetype-dev@edge \
      harfbuzz@edge \
      ttf-freefont@edge && \
    pip3 install -U pip setuptools wheel

    RUN delgroup ping && \
        addgroup --gid <DOCKER_GID> docker && \
        adduser --system --uid <DOCKER_UID> --ingroup docker <$USER> && \
        addgroup <$USER> dialout

RUN chmod -R 770 /config && \
    chmod +x /usr/src/app/docker-entrypoint.sh && \
    chown -R <$USER>:docker /config /home/<$USER>

RUN setfacl -R -m d:u:<$USER>:rwX,d:g:docker:rwX,d:o::--- /config && \
    setfacl -R -m d:u:<$USER>:rwX,d:g:docker:rwX,d:o::--- /home/<$USER>

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
CMD ["python3","-m","homeassistant","-c","/config"]
