import asyncio


async def generate_remote_data(delay, *args):
    for x, y in args:
        for i in range(x, y):
            yield {'id': i, 'name ': 'Test {}'.format(i)}
            await asyncio.sleep(delay)
