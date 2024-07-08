"""
This script retrieves and prints metadata profile information from a Nostr relay for a given public key (npub).

Usage:
    python nostr_info.py 

Requirements:
    - nostr library
    - Python 3.x

Example:
    python nostr_info.py 
"""
import time, uuid, ssl, json
from nostr.event import EventKind
from nostr.relay_manager import RelayManager
from nostr.key import PublicKey
from nostr.filter import Filter, Filters
from nostr.message_type import ClientMessageType

def get_info():
    pub_key = PublicKey.from_npub('npub1mwce4c8qa2zn9zw9f372syrc9dsnqmyy3jkcmpqkzaze0slj94dqu6nmwy')
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
        print(json.dumps(json.loads(event_msg.event.content), indent=4))

    relay_manager.close_connections()

if __name__ == "__main__":
    get_info()
