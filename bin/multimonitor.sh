#!/usr/bin/bash
#xrandr --newmode 1920x1080_60  173.00  1920 2048 2248 2576  1080 1083 1088 1120 -hsync +vsync
#xrandr --addmode HDMI1 1920x1080_60
QTD_MONITORS=$(xrandr | grep -sw connected | wc -l)
if [ $QTD_MONITORS -gt 1 ]; then
	FIRST=$(xrandr | grep -sw connected | awk '{print $1}' | sed -n "1p")
	SECOND=$(xrandr | grep -sw connected | awk '{print $1}' | sed -n "2p")
	#xrandr --output eDP-1 --primary --mode 1366x768 --pos 1920x312 --rotate normal --output HDMI-1 --mode 1920x1080 --pos 0x0 --rotate normal
	xrandr --output $FIRST --primary --mode 1366x768 --pos 1920x312 --rotate normal --output $SECOND --mode 1920x1080 --pos 0x0 --rotate normal
fi
