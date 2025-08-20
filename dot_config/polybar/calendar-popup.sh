#!/bin/sh

BAR_HEIGHT=22  # polybar height
BORDER_SIZE=1  # border size from your wm settings
YAD_WIDTH=222  # 222 is minimum possible value
YAD_HEIGHT=193 # 193 is minimum possible value
DATE="$(date +"%a %d %H:%M")"

case "$1" in
--popup)
    if [ "$(xdotool getwindowfocus getwindowname)" = "yad-calendar" ]; then
        exit 0
    fi
    # Detecta se está rodando bspwm
    if command -v bspc >/dev/null 2>&1 && bspc wm -d >/dev/null 2>&1; then
        # Pega posição do mouse e resolução da tela
        eval "$(xdotool getmouselocation --shell)"
        eval "$(xdotool getdisplaygeometry --shell)"

        # Calcula posição X (tenta centralizar a janela no mouse, respeitando limites)
        if [ "$((X + YAD_WIDTH / 2 + BORDER_SIZE))" -gt "$WIDTH" ]; then
            pos_x=$((WIDTH - YAD_WIDTH - BORDER_SIZE))
        elif [ "$((X - YAD_WIDTH / 2 - BORDER_SIZE))" -lt 0 ]; then
            pos_x=$BORDER_SIZE
        else
            pos_x=$((X - YAD_WIDTH / 2))
        fi

        # Calcula posição Y (se mouse estiver na metade inferior da tela, abre acima, senão abaixo da barra)
        if [ "$Y" -gt "$((HEIGHT / 2))" ]; then
            pos_y=$((HEIGHT - YAD_HEIGHT - BAR_HEIGHT - BORDER_SIZE))
        else
            pos_y=$((BAR_HEIGHT + BORDER_SIZE))
        fi

        # Abre yad com posição fixa, título para detectar no bspwm e sem borda
        yad --calendar --title="yad-calendar" --borders=0 --button=Ok:1 --close-on-unfocus \
            --width="$YAD_WIDTH" --height="$YAD_HEIGHT" --posx="$pos_x" --posy="$pos_y" >/dev/null &
    else
        yad --calendar --title="yad-calendar" --borders=0 --button=Ok:1 --close-on-unfocus >/dev/null &
    fi
    ;;
*)
    echo "$DATE"
    ;;
esac
