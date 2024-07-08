#!/usr/bin/env python3
"""
This script updates the profile picture of a user using the provided nsec (private key) and picture URL.

Usage:
    python update_profile_picture.py [nsec] [picture_url]

Arguments:
    nsec        : The private key of the user (in nsec format).
    picture_url : The URL of the new profile picture.

Requirements:
    - nostr library
    - Python 3.x

Example:
    python update_profile_picture.py nsec1... "https://example.com/picture.jpg"
"""

import argparse
import time
import ssl
import json
from nostr.key import PrivateKey
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager

def update_profile_picture(nsec, picture_url):
    private_key = PrivateKey.from_nsec(nsec)
    public_key = private_key.public_key.hex()

    metadata_content = {
        "picture": picture_url
    }

    event = Event(
        public_key=public_key,
        kind=EventKind.SET_METADATA,
        content=json.dumps(metadata_content)
    )
    private_key.sign_event(event)

    relay_manager = RelayManager()
    relay_manager.add_relay("wss://relay.damus.io")
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})
    time.sleep(1.25)  # Allow time for connections to open

    relay_manager.publish_event(event)
    time.sleep(1)  # Allow time for the message to send

    relay_manager.close_connections()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update the profile picture of a user using the provided nsec (private key) and picture URL.')
    parser.add_argument('nsec', type=str, help='The private key of the user (in nsec format).')
    parser.add_argument('picture_url', type=str, help='The URL of the new profile picture.')
    args = parser.parse_args()
    update_profile_picture(args.nsec, args.picture_url)

