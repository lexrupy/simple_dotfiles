# xrandr --addmode VIRTUAL1 1024x768
# xrandr --addmode VIRTUAL1 1280x720
# xrandr --addmode VIRTUAL1 1366x768
# xrandr --addmode VIRTUAL1 1440x900
# xrandr --addmode VIRTUAL1 720x400
xrandr --newmode "1000x450"   34.75  1000 1024 1120 1240  450 453 463 469 -hsync +vsync
xrandr --addmode VIRTUAL1 1000x450
xrandr --output VIRTUAL1 --mode 1000x450 --below HDMI1
