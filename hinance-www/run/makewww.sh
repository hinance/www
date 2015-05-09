#!/bin/bash

set -e

TMPDIR=/var/tmp/hinance-www

# main static content
cp /hinance-www/www/* $TMPDIR

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

# examples
cd $TMPDIR
#TODO: add examples here
