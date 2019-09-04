#!/bin/bash
set -e

python3 -m homeassistant -c /config --script check_config
exec gosu <$USER>:docker "$@"
