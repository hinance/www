#!/bin/bash

set +e
echo "Restarting."
docker stop hinance-www
docker rm hinance-www
set -e

mkdir -p /var/tmp/hinance-www
chown 1000:1000 /var/tmp/hinance-www

docker run --rm -t \
    -v /etc/localtime:/etc/localtime:ro \
    -v /etc/hinance-www:/etc/hinance-www:ro \
    -v /var/tmp/hinance-www:/var/tmp/hinance-www \
    --name hinance-www -h hinance-www \
    hinance/hinance-www:0 \
    sudo -iu user /hinance-www/run/run.sh
