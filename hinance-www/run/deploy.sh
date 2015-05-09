#!/bin/bash

set -e

. /etc/hinance-www/config.sh

mkdir -p /home/user/.ssh
echo "$ID_RSA_PUB" > /home/user/.ssh/id_rsa.pub
echo "$ID_RSA" > /home/user/.ssh/id_rsa
chmod 600 /home/user/.ssh/id_rsa
cp /hinance-www/setup/known_hosts /home/user/.ssh

echo "$URL" > /var/tmp/hinance-www/CNAME

cd /var/tmp/hinance-www
rm -rf .git
git init
git config user.email "$GIT_EMAIL"
git config user.name "$GIT_USER"
git add .
git commit -m "Automatic deploy."
git remote add origin $GIT_REPO
git push -f origin master
