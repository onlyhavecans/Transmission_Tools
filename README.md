#My Transmission scripts
I thought I should share these out in one repo just to help... Also, don't pirate kids.


# Update Blacklists
This one is the simplest. Use some expansion to download the most popular conprehensive blacklists and restart transmission. I recommend only doing this once a day at most.


# Move & Stop Finished Torrents
This script in it's simplest form acts as a cleanup for your old torrents.
It copies all of your torrents that have finished seeding to an archive directory and then removes the torrents and the old files.

Not so hidden in this script is a super useful TransmissionRequestWrapper class that can be used for all sorts of other cool transmission scripts. It's the closest thing to an API I am willing to write... at the moment.


## Installation & Usage
1. Put the file somewhere safe
2. Edit the destination for old torrents and set rpc username and password as needed
3. Make sure it is executable
4. Set the following in transmission's settings.json
    - set script-torrent-done-enabled: True
        - script-torrent-done-filename: "Path/to/script"
        5. Restart Transmission

        If you are having problems configuring transmission see https://trac.transmissionbt.com/wiki/EditConfigFiles

## Notes
This script assumes a few things;

1. it is running on the same box as transmission
2. Set as script-torrent-done-filename OR cron it, it doesn't require any vars
3. While it is hypothetically windows compatible it's untested
4. Most importantly, you set Username, Password and Dest Directory
5. No username & Password is put in as None not ""
6. No third party libraries needed but 2.6+ recommended
