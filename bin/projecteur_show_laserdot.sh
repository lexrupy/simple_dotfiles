#!/bin/bash

if pgrep -x "projecteur" > /dev/null
then
    projecteur -c zoom=false
    projecteur -c dot=true
    projecteur -c shade=false
    projecteur -c border=false
    projecteur -c dot.color=#FF0000
    projecteur -c spot=on
fi
