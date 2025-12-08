#!/bin/bash
#
# script that paraphtases info from the debian wiki at: https://wiki.debian.org/ppviewerFonts
#
#
set -e

DOWNLOAD_URL="https://archive.org/download/PowerPointViewer_201801/PowerPointViewer.exe"
EXPECTED_CHECKSUM="249473568eba7a1e4f95498acba594e0f42e6581add4dead70c1dfb908a09423"
FONT_DIR="$HOME/.local/share/fonts/ppviewer"

echo "Installing PowerPoint Fonts..."

command -v cabextract >/dev/null || { echo "Installing cabextract..."; sudo apt update && sudo apt install -y cabextract; }

echo "Downloading PowerPoint Viewer..."
wget -q "$DOWNLOAD_URL"
ACTUAL_CHECKSUM=$(sha256sum PowerPointViewer.exe | cut -d' ' -f1)
[ "$ACTUAL_CHECKSUM" = "$EXPECTED_CHECKSUM" ] || { echo "Checksum verification failed!"; rm -f PowerPointViewer.exe; exit 1; }

echo "Installing fonts..."
cabextract PowerPointViewer.exe -F ppviewer.cab >/dev/null
mkdir -p "$FONT_DIR"
cabextract ppviewer.cab -F '*.TTC' -F '*.TTF' -d "$FONT_DIR" >/dev/null

rm -f PowerPointViewer.exe ppviewer.cab

echo "Fonts installed to: $FONT_DIR"
echo "Restart applications to use new fonts."
