import asyncio
from nostr_sdk import Client, PublicKey, Filter, Kind
from datetime import timedelta
import json
import argparse

async def fetch_profile(npub):
    client = Client()
    await client.add_relay("wss://relay.damus.io")
    await client.connect()

    pk = PublicKey.from_bech32(npub)
    filter = Filter().kind(Kind(0)).author(pk).limit(1)
    events = await client.get_events_of([filter], timedelta(seconds=10))

    if events:
        metadata = json.loads(events[0].content())
        print(f"Metadata for {npub}:")
        for key, value in metadata.items():
            print(f"{key}: {value}")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
    else:
        print(f"No profile found for {npub}.\n")
    return

async def fetch_profiles_from_file(filename):
    with open(filename, 'r') as file:
        npub_keys = [line.strip() for line in file.readlines()]

    tasks = [fetch_profile(npub) for npub in npub_keys]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch metadata for a list of npub keys from a file.')
    parser.add_argument('filename', type=str, help='File containing a list of npub keys.')
    args = parser.parse_args()

    asyncio.run(fetch_profiles_from_file(args.filename))

