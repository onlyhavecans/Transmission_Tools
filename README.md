# My Transmission scripts
Don't pirate kids.

That said I run a [Transmission](http://www.transmissionbt.com/) bittorrent server to help grab up all the random files on the internet and also to help seed projects I "support". Here is the collections of scripts I use to help automate it, because everything needs automation.

## Update Blacklists
Download the most popular conprehensive blacklists and restart transmission.
This one is simple and can be hacked to add more at your liesure, but should be runnable as is. I recommend cronning this to once a day at 3AM


## Move & Stop Finished Torrents
"ProcessFinishedTorrents.py" verifies your completed torrents, moves them to a pickup/transfer directory, and then removes and cleans it out of tranmsission.
This is great if you use a blanket stop seeding ratio and don't want to have to manually clean everything out. Use it with a dropbox or rsync transfer folder to get your files delevered to your workstation when they are fully complete.


Not so hidden in this script is a super useful TransmissionRequestWrapper class that can be used for all sorts of other cool transmission scripts. It's the closest thing to an API I am willing to write... at the moment.


### Installation & Usage
1. Edit the destination for old torrents and set rpc username and password as needed
2. Make sure it is executable
3. Set the following in transmission's settings.json
    - set script-torrent-done-enabled: True
    - script-torrent-done-filename: "Path/to/script"
4. Restart Transmission

        If you are having problems configuring transmission see https://trac.transmissionbt.com/wiki/EditConfigFiles

### Notes
This script assumes a few things;

1. it is running on the same box as transmission, thought that can be fixed with a vew small tweaks
2. Set as script-torrent-done-filename or cron it, it doesn't require any vars
3. While it is hypothetically windows compatible it's untested
4. No username & Password is put in as None not ""
5. No third party libraries needed but 2.6+ recommended, I have been adding python 3 compatibility
