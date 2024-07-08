import asyncio
from nostr_sdk import Client, NostrSigner, Keys, PublicKey, EventBuilder, init_logger, LogLevel
import argparse

async def send_direct_message(nsec, recipient_npub, message):
    init_logger(LogLevel.INFO)
    keys = Keys.parse(nsec)
    signer = NostrSigner.keys(keys)
    client = Client(signer)
    await client.add_relay("wss://relay.damus.io")
    await client.connect()
    
    recipient_pk = PublicKey.from_bech32(recipient_npub)
    
    # Use EventBuilder to create the direct message event
    dm = EventBuilder.encrypted_direct_msg(
        sender_keys=keys.parse(nsec),
        receiver_pubkey=recipient_pk,
        content=message
    )
    await client.send_event_builder(dm)
    
    await asyncio.sleep(10)
    #await client.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a direct message using Nostr SDK.')
    parser.add_argument('nsec', type=str, help='The private key of the sender (in nsec format).')
    parser.add_argument('recipient_npub', type=str, help='The npub of the recipient.')
    parser.add_argument('message', type=str, help='The message to send.')
    args = parser.parse_args()

    asyncio.run(send_direct_message(args.nsec, args.recipient_npub, args.message))

