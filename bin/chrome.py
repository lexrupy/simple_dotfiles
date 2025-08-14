#!/usr/bin/env python3
import subprocess
import time
import sys


def get_chrome_wids():
    try:
        output = subprocess.check_output(
            ["xdotool", "search", "--class", "Google-chrome"]
        )
        return set(map(int, output.split()))
    except subprocess.CalledProcessError:
        return set()


def open_chrome_new_window(profile):
    before = get_chrome_wids()

    # Lança o Chrome
    subprocess.Popen(
        ["google-chrome", "--new-window", f"--profile-directory={profile}"]
    )

    # Espera até aparecer um WID novo
    new_wid = None
    while new_wid is None:
        time.sleep(0.1)
        after = get_chrome_wids()
        diff = after - before
        if diff:
            new_wid = diff.pop()
    return new_wid


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 open_chrome.py <ProfileName>", file=sys.stderr)
        sys.exit(1)

    profile = sys.argv[1]
    wid = open_chrome_new_window(profile)
    # print(f"Nova janela do Chrome (profile={profile}) WID: {wid}")
    print(wid)
