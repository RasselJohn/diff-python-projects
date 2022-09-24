import argparse
import asyncio
import random

import websockets
from websockets.exceptions import ConnectionClosed


async def handler(host, client_id):
    uri = f'{host}?client_id={client_id}'
    async with websockets.connect(uri) as ws:
        session_id = await ws.recv()
        print(f'{session_id=}')

        try:
            while True:
                message = f'{random.randint(0, 100)}'
                print(f'{message=}')
                await ws.send(message)
                await asyncio.sleep(1)
        except ConnectionClosed:
            print('Connection closed...')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WS client.')
    parser.add_argument('--endpoint', dest='url', default='ws://localhost:8880')
    parser.add_argument('--client-id', dest='client_id', default='test1')
    args = parser.parse_args()
    asyncio.run(handler(args.url, args.client_id))
