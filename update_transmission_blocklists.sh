#!/usr/bin/env bash

BLOCKLIST_DIR="$HOME/.config/transmission-daemon/blocklists"

## Put Overrides for the above in this file
source "$HOME/.config/blocklists.conf"

cd "$BLOCKLIST_DIR" || exit 1

curl -L \
	http://list.iblocklist.com/?list=bt_level[1-3] \
	-o "bt_level#1.gz"

gunzip -f ./*.gz

killall -HUP transmission-daemon
