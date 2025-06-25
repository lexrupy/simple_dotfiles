#!/bin/bash

# Alvo: classe da janela
TARGET_CLASS="ChatNavigator"

# Foca na janela com a classe desejada
i3-msg "[class=\"$TARGET_CLASS\"] focus"

# Move a janela repetidamente para a esquerda
# Isso é uma heurística: repete algumas vezes para garantir o movimento máximo
i3-msg move left
i3-msg move left
