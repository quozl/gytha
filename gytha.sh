#!/bin/sh
cd /usr/share/games/gytha
PATH=$PATH:/usr/share/games/gytha
exec gytha.py $*
