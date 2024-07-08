#!/usr/bin/env python3
"""
This script sends a note with the provided text using the provided nsec (private key).

Usage:
    python send_note.py [nsec] [note_text]

Arguments:
    nsec      : The private key of the user (in nsec format).
    note_text : The text content of the note to be sent.

Requirements:
    - nostr library
    - Python 3.x

Example:
    python send_note.py nsec1... "hello world"
"""

import argparse
import time
import ssl
from nostr.key import PrivateKey
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager

def send_note_nsec(nsec, note_text):
    private_key = PrivateKey.from_nsec(nsec)
    public_key = private_key.public_key.hex()

    event = Event(
        public_key=public_key,
        kind=EventKind.TEXT_NOTE,
        content=note_text
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
    parser = argparse.ArgumentParser(description='Send a note using the provided nsec (private key).')
    parser.add_argument('nsec', type=str, help='The private key of the user (in nsec format).')
    parser.add_argument('note_text', type=str, help='The text content of the note to be sent.')
    args = parser.parse_args()
    send_note_nsec(args.nsec, args.note_text)

