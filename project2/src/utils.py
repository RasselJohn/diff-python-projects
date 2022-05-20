from typing import Generator, Callable, Any

import asyncio
from yarl import URL

# in seconds
REQUEST_TIMEOUT = 5

# in seconds
# if it would be more REQUEST_TIMEOUT - timeout can happen
MAX_RANDOM_TIMEOUT = 4


def generate_remote_data(*args) -> Generator[None, dict, None]:
    for x, y in args:
        for i in range(int(x), int(y)):
            yield {'id': i, 'name ': 'Test {}'.format(i)}


def set_timeout(timeout: int) -> Callable[..., Any]:
    def wrap(func) -> Callable[..., Any]:
        async def sub_wrap(*args) -> None:
            try:
                await asyncio.wait_for(func(*args), timeout=timeout)
            except asyncio.TimeoutError:
                print("Timeout! Data don't load!")
            except Exception:
                pass

        return sub_wrap

    return wrap
