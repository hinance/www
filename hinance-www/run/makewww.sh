#!/bin/bash

set -e

TMPDIR=/var/tmp/hinance-www

# main static content
cp -r /hinance-www/www/* $TMPDIR

# bootstrap
cd /hinance-www/bootstrap.git
git checkout .
git apply /hinance-www/setup/bootstrap/bootstrap.patch
grunt dist
cp -r /hinance-www/bootstrap.git/dist/* $TMPDIR

# jquery
cp -r /hinance-www/jquery/node_modules/jquery/dist/cdn/* $TMPDIR

# pics
convert $TMPDIR/oleg.jpg -strip -rotate 90 -resize 160x120 $TMPDIR/oleg-sm.jpg

#
# examples
#

function runexample() {
  cd $1
  hinance &
  PID1=$!
  tail -F out/log/hinance.log &
  PID2=$!
  while ! grep "Cycle finished" out/log/hinance.log &>/dev/null ; do
    sleep 1
  done
  kill $PID1 $PID2
}

weboob-config update
runexample $TMPDIR/examples/min
runexample $TMPDIR/examples/max
