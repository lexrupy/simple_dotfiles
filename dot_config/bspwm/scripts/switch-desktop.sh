#!/bin/sh

KEY="$1"
ACTION="$2"   # "focus" ou "send"

# Conta monitores
MONS="$(bspc query -M | wc -l)"

# Se 3 monitores → usa ordem alterada
if [ "$MONS" -eq 3 ]; then
    case "$KEY" in
        1) D=4 ;;
        2) D=5 ;;
        3) D=6 ;;
        4) D=7 ;;
        5) D=8 ;;
        6) D=9 ;;
        7) D=10 ;;
        8) D=1 ;;
        9) D=2 ;;
        0) D=3 ;; # zero
    esac
else
    # ordem padrão
    case "$KEY" in
        1) D=1 ;;
        2) D=2 ;;
        3) D=3 ;;
        4) D=4 ;;
        5) D=5 ;;
        6) D=6 ;;
        7) D=7 ;;
        8) D=8 ;;
        9) D=9 ;;
        0) D=10 ;; # zero vira 10
    esac
fi

# Executa
if [ "$ACTION" = "send" ]; then
    bspc node -d "^$D" --follow
else
    bspc desktop -f "^$D"
fi

