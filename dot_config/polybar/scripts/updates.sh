#!/usr/bin/env bash

# Contar atualizações APT
# APT=$(apt list --upgradable 2>/dev/null | grep -c upgradable)

APT=$(apt update -o Dir::Etc::SourceList=/dev/null -o Dir::Etc::SourceParts=/dev/null -o APT::Get::List-Cleanup=0 >/dev/null 2>&1 ; apt list --upgradable 2>/dev/null | grep -c upgradable)

# Contar atualizações Flatpak
FLATPAK=$(flatpak remote-ls --updates 2>/dev/null | wc -l)

TOTAL=$((APT + FLATPAK))


if [ "$TOTAL" -eq 0 ]; then
    # verde
    echo "%{F#00ff00} 0%{F-}"
else
    # vermelho
    echo "%{F#ff5555} $TOTAL%{F-}"
fi
