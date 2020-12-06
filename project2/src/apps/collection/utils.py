import asyncio
from typing import Generator


async def generate_remote_data(delay: int, *args) -> Generator[None, dict, None]:
    for x, y in args:

        for i in range(x, y):
            yield {'id': i, 'name ': 'Test {}'.format(i)}

            await asyncio.sleep(delay)
