#!/bin/bash
if pgrep -x "projecteur" > /dev/null
then
    projecteur -c zoom=false
    projecteur -c dot=false
    projecteur -c shade=true
    projecteur -c border=true
    projecteur -c border.color=#FF0000
    projecteur -c border.size=2
    projecteur -c spot.overlay=true
    projecteur -c spot.size=30
    projecteur -c spot=on
fi
