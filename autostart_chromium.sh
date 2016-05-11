#!/bin/sh
unclutter &
matchbox-window-manager & :
xset -dpms
xset s off
#while true; do
#/usr/bin/midori -e Fullscreen
#epiphany-browser -a --profile ~/.config http://localhost/index.html
/usr/bin/chromium-browser --kiosk --incognito http://127.0.0.1 http://127.0.0.1/others http://127.0.0.1/kalender
done

