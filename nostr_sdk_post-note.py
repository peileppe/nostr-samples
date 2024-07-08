import asyncio
from nostr_sdk import Client, NostrSigner, Keys, EventBuilder, init_logger, LogLevel
import argparse

async def post_note_to_feed(nsec, note_content):
    init_logger(LogLevel.INFO)
    keys = Keys.parse(nsec)
    signer = NostrSigner.keys(keys)
    client = Client(signer)
    await client.add_relay("wss://relay.damus.io")
    await client.connect()
    
    # Use EventBuilder to create the note event
    note_event = EventBuilder.text_note(
        content=note_content,
        tags=[]
    )
    await client.send_event_builder(note_event)
    
    await asyncio.sleep(10)
    #await client.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Post a note to the user feed using Nostr SDK.')
    parser.add_argument('nsec', type=str, help='The private key of the user (in nsec format).')
    parser.add_argument('note_content', type=str, help='The content of the note to post.')
    args = parser.parse_args()

    asyncio.run(post_note_to_feed(args.nsec, args.note_content))

