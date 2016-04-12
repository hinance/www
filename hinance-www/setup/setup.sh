#!/bin/bash
set -e
pacman -S --noconfirm --needed imagemagick nodejs npm openssh
chown -R user:user /hinance-www
sudo -u user bash -l /hinance-www/setup/as-user.sh
paccache -rk0
