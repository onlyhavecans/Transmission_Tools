#!/bin/sh

cd "$HOME/.config/transmission-daemon/blocklists"

curl -L \
	http://list.iblocklist.com/?list=bt_level[1-3] \
	-o "bt_level#1.gz"
gunzip -f *.gz

killall -HUP transmission-daemon
