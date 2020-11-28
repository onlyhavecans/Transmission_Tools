#!/usr/bin/env bash

BLOCKLIST_DIR="$HOME/.config/transmission-daemon/blocklists"

if [[ -d "/usr/local/var/transmission/blocklists" ]]; then
  BLOCKLIST_DIR="/usr/local/var/transmission/blocklists"
fi

CONFIG="$HOME/.config/blocklists.conf"

## Put Overrides for the above in this file
if [[ -f "$CONFIG" ]]; then
  source "$CONFIG"
fi

cd "$BLOCKLIST_DIR" || exit 1

curl -L --silent --show-error \
	https://list.iblocklist.com/?list=bt_level[1-3] \
	-o "bt_level#1.gz"

gunzip -f ./*.gz

killall -HUP transmission-daemon
