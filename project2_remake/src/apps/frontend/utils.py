import asyncio
from typing import Generator, Callable, Any


def generate_remote_data(*args) -> Generator[None, dict, None]:
    for x, y in args:
        for i in range(int(x), int(y)):
            yield {'id': i, 'name ': 'Test {}'.format(i)}


def set_timeout(delay: int) -> Callable[..., Any]:
    def wrap(func):
        async def sub_wrap(*args):
            try:
                await asyncio.wait_for(func(*args), timeout=delay)
            except asyncio.TimeoutError:
                print("Timeout! Data don't load!")
            except Exception:
                pass

        return sub_wrap

    return wrap
