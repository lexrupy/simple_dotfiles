#!/bin/sh
KEY="$1"

MONS="$(bspc query -M | wc -l)"

if [ "$MONS" -eq 3 ]; then
    case "$KEY" in
        1) echo 4 ;;
        2) echo 5 ;;
        3) echo 6 ;;
        4) echo 7 ;;
        5) echo 8 ;;
        6) echo 9 ;;
        7) echo 10 ;;
        8) echo 1 ;;
        9) echo 2 ;;
        0) echo 3 ;;
        *) echo "$KEY" ;;
    esac
else
    [ "$KEY" -eq 0 ] && echo 10 || echo "$KEY"
fi

