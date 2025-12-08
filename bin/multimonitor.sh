#!/usr/bin/bash

PRIMARY="HDMI-1"

QTD_MONITORS=$(xrandr | grep -sw connected | wc -l)
if [ $QTD_MONITORS -gt 2 ]; then
	FIRST=$(xrandr | grep -sw connected | awk '{print $1}' | sed -n "1p")
	SECOND=$(xrandr | grep -sw connected | awk '{print $1}' | sed -n "2p")
	THIRD=$(xrandr | grep -sw connected | awk '{print $1}' | sed -n "3p")
  xrandr \
  	--output $FIRST --primary --mode 1366x768 --pos 2474x0 --rotate normal \
  	--output $SECOND --mode 1920x1080 --pos 0x768 --rotate normal \
  	--output $THIRD --mode 1920x1080 --pos 1920x768 --rotate normal
elif [ $QTD_MONITORS -gt 1 ]; then
	FIRST=$(xrandr | grep -sw connected | awk '{print $1}' | sed -n "1p")
	SECOND=$(xrandr | grep -sw connected | awk '{print $1}' | sed -n "2p")
	#
	#xrandr --output eDP-1 --primary --mode 1366x768 --pos 1920x312 --rotate normal --output HDMI-1 --mode 1920x1080 --pos 0x0 --rotate normal
	# Tela notebook na direita
	# xrandr --output $FIRST --primary --mode 1366x768 --pos 1920x312 --rotate normal --output $SECOND --mode 1920x1080 --pos 0x0 --rotate normal
	# Tela notebook na esquerda
	xrandr --output $FIRST --primary --mode 1366x768 --pos 0x0 --rotate normal --output $SECOND --mode 1920x1080 --pos 1366x0 --rotate normal
fi




