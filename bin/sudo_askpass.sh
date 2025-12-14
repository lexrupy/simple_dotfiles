#!/bin/bash
#
# sudo-askpass - prompt gráfico ou TTY para senha do sudo
#

PROMPT="Authentication required for $USER"

get_pass() {
    # Função auxiliar para garantir printf limpo
    printf "%s" "$1"
}

# yad
if command -v yad >/dev/null 2>&1; then
    PASSWORD="$(yad \
        --entry \
        --entry-label "Password" \
        --hide-text \
        --image=password \
        --window-icon=dialog-password \
        --text="$PROMPT" \
        --title="Authentication" \
        --center)"
    get_pass "$PASSWORD"
    exit
fi

# zenity
if command -v zenity >/dev/null 2>&1; then
    PASSWORD="$(zenity --password --title="$PROMPT")"
    get_pass "$PASSWORD"
    exit
fi

# kdialog
if command -v kdialog >/dev/null 2>&1; then
    PASSWORD="$(kdialog --password "$PROMPT")"
    get_pass "$PASSWORD"
    exit
fi

# TTY fallback
STTY_SAVE=$(stty -g)
trap 'stty "$STTY_SAVE"' EXIT

printf "Enter password for %s: " "$USER" > /dev/stderr
stty -echo
read -r PASSWORD
stty "$STTY_SAVE"
printf "\n"

get_pass "$PASSWORD"

