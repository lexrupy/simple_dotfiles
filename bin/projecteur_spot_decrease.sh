#!/bin/bash

if pgrep -x "projecteur" > /dev/null
then
    projecteur -c spot.size.adjust=-5
fi
