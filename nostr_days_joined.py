#!/usr/bin/env python3
"""
Fetches the joined date from a Nostr profile and calculates the days since account creation.

Usage:
    python fetch_joined_date.py [npub]

Arguments:
    npub : The public key of the user (in npub format).

Requirements:
    - nostr library
    - Python 3.x

Example:
    python fetch_joined_date.py npub1...
"""

import argparse, time, ssl, json, uuid
from datetime import datetime
from nostr.event import EventKind
from nostr.relay_manager import RelayManager
from nostr.key import PublicKey
from nostr.filter import Filter, Filters
from nostr.message_type import ClientMessageType

def get_info(npub):
    pub_key = PublicKey.from_npub(npub)
    metadata=None
    filters = Filters([Filter(authors=[pub_key.hex()], kinds=[EventKind.SET_METADATA])])
    subscription_id = uuid.uuid1().hex
    request = [ClientMessageType.REQUEST, subscription_id, *filters.to_json_array()]
    relay_manager = RelayManager()
    relay_manager.add_relay("wss://relay.damus.io")
    relay_manager.add_subscription(subscription_id, filters)
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})
    time.sleep(1.25)
    relay_manager.publish_message(json.dumps(request))
    time.sleep(1)
    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()
        metadata=(json.loads(event_msg.event.content))
    relay_manager.close_connections()
    return metadata

def fetch_joined_date(npub):
    metadata=get_info(npub)
    print(metadata)
    print(type(metadata))
    created_at = metadata['created_at']
    print(created_at)
    if created_at:
        created_date = datetime.utcfromtimestamp(created_at)
        days_since_creation = (datetime.utcnow() - created_date).days
        print(f"Account created on: {created_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"Days since account creation: {days_since_creation}")
        return
    print("Could not retrieve metadata created_at")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch the joined date from a Nostr profile and calculate the days since account creation.')
    parser.add_argument('npub', type=str, help='The public key of the user (in npub format).')
    args = parser.parse_args()
    fetch_joined_date(args.npub)

