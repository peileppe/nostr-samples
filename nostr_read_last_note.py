#!/usr/bin/env python3
"""
Logs in with the public key (npub) and reads the last note posted by the user.

Usage:
    python nostr_read_last_note.py [public_key]

Arguments:
    public_key : The public key of the user (in npub format). Defaults to a predefined value.

Requirements:
    - nostr library
    - Python 3.x

Example:
    python nostr_read_last_note.py npub1...
"""

import argparse, time, ssl, json
from nostr.event import EventKind
from nostr.relay_manager import RelayManager
from nostr.key import PublicKey
from nostr.filter import Filter, Filters
from nostr.message_type import ClientMessageType

DEFAULT_NPUB = 'npub1mwce4c8qa2zn9zw9f372syrc9dsnqmyy3jkcmpqkzaze0slj94dqu6nmwy'

def read_last_note(public_key_str):
    filters = Filters([Filter(authors=[PublicKey.from_npub(public_key_str).hex()], kinds=[EventKind.TEXT_NOTE], limit=1)])
    request = [ClientMessageType.REQUEST, 'subscription-id', *filters.to_json_array()]
    relay_manager = RelayManager()
    relay_manager.add_relay("wss://relay.damus.io")
    relay_manager.add_subscription('subscription-id', filters)
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})
    time.sleep(1.25)
    relay_manager.publish_message(json.dumps(request))
    time.sleep(1)
    if relay_manager.message_pool.has_events():
        print("Last Note:", relay_manager.message_pool.get_event().event.content)
    else:
        print("No notes found.")
    relay_manager.close_connections()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Log in with the public key and read the last note posted by the user.')
    parser.add_argument('public_key', type=str, nargs='?', default=DEFAULT_NPUB, help='The public key of the user (in npub format). Defaults to a predefined public key.')
    read_last_note(parser.parse_args().public_key)

