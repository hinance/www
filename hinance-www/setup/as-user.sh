#!/bin/bash

set -e

. /hinance-docker/setup/share.sh

# grunt-cli
sudo npm install -g grunt-cli@0.1.13

# bootstrap
git clone https://github.com/twbs/bootstrap /hinance-www/bootstrap.git
cd /hinance-www/bootstrap.git
git checkout v3.3.4
npm install

# jquery
mkdir /hinance-www/jquery
cd /hinance-www/jquery
npm install jquery@1.11.2
