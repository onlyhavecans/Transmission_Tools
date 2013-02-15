#!/usr/bin/env python
# encoding: utf-8
"""
Created by tBunnyMan on 2012-03-28.
Copyright (c) 2012 Bunni.biz. All rights reserved.

This script assumes a few things;
1. it is running on the same box as transmission
2. Set as script-torrent-done-filename OR cron it, it doesn't require any vars
3. While it is hypothetically windows compatible it's untested
4. Most importantly, you set Username, Password and Dest Directory
5. No username & Password is put in as None not ""
"""

import json
import shutil
import urllib2
import urllib
import os
import re


DESTINATION_DIRECTORY = "/Users/bunnyman/Dropbox/Shared/Torrent Out/"
USER = "admin"
PASSWD = "bunny"

class TransmissionRequestWrapper(object):
    """
    This is a code saver for sending json requests to Transmission
    You only need to instantiate one per server and use json_request to send
     commands
    """
    def __init__(self, username=None, password=None,
                 host="localhost", port="9091", path="transmission/rpc/"):
        """
        Load up the variables, get the session ID, optionally load up
         urllib2's auth with the needed username and password
        """
        if username is None or password is None:
            self._noPass = True
        else:
            self._username = username
            self._password = password
            self._noPass = False
        self._host = host
        self._port = port
        self._path = path
        self._sessionID = self.get_session_id()
        self._url = "http://%s:%s/%s" % (self._host, self._port, self._path)
        if self._noPass is False:
            authHandler = urllib2.HTTPPasswordMgrWithDefaultRealm()
            authHandler.add_password(None, self._url, self._username, self._password)
            opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(authHandler))
            urllib2.install_opener(opener)

    def get_session_id(self):
        """
        Establish a Transmission Session ID before sending anything
        Use urllib instead of urllib2 because it can't cleanly handle the 409
        """
        if self._noPass:
            url = self._url
        else:
            url = "http://%s:%s@%s:%s/%s" % (self._username, self._password,
                                             self._host, self._port, self._path)
        req = urllib.urlopen(url)
        rawData = req.read()
        pattern = re.compile('X-Transmission-Session-Id: ([a-zA-Z0-9]+)')
        sessionID = pattern.search(rawData)
        if not sessionID:
            raise Exception("Unable to get session id!")
        return {'x-transmission-session-id': sessionID.group(1)}

    def json_request(self, jsonRequest):
        """
        This takes a dictionary, encodes it with json, and sends to
         transmission with the session ID & Auth as needed.

        It returns the reply as a dictionary.

        See https://trac.transmissionbt.com/wiki/rpc for the Specification
        """
        encodedJson = json.dumps(jsonRequest)
        encodedRequest = urllib2.Request(self._url, encodedJson, self._sessionID)
        rawData = urllib2.urlopen(encodedRequest)
        return json.load(rawData)


def main():
    """
    Kittens!
    """
    connection = TransmissionRequestWrapper(USER, PASSWD)

    getRequest = {
        "method": "torrent-get",
        "arguments": {
            "fields": ["id", "name", "haveValid", "totalSize",
                       "isFinished", "downloadDir"
            ]
        }
    }

    getResponse = connection.json_request(getRequest)
    for torrent in getResponse["arguments"]["torrents"]:
        if not torrent["isFinished"]:
            continue
        if not torrent["haveValid"] == torrent["totalSize"]:
            print "Torrent %s was finished but valid does not match restarting" % torrent["name"]
            verifyRequest = {
                "method": "torrent-verify",
                "arguments": {
                    "ids": [torrent["id"]]
                }
            }
            reply = connection.json_request(verifyRequest)
            print "Torrent %s verifying: %s" % (
                torrent["name"], reply["result"])
            continue

        print "Torrent %s finished" % (torrent["name"])
        shutil.copytree(
            os.path.join(torrent["downloadDir"], torrent["name"]),
            os.path.join(DESTINATION_DIRECTORY, torrent["name"])
            )

        removeRequest = {
            "method": "torrent-remove",
            "arguments": {
                "ids": torrent["id"],
                "delete-local-data": True
            }
        }
        status = connection.json_request(removeRequest)
        print "%s moved and deleted: %s" % (torrent["name"], status["result"])
        print "\n"


if __name__ == '__main__':
    main()
