import asyncio
import json
import random
from pprint import pprint

from aiohttp import web, ClientSession
from yarl import URL

from src.utils import set_timeout, REQUEST_TIMEOUT, MAX_RANDOM_TIMEOUT


class IndexView(web.View):
    BOUNDS = [(1, 11, 31, 41), (11, 21, 41, 51), (21, 31, 51, 61)]

    async def get(self) -> web.Response:
        self.result: list[str] = []
        urls: list[str] = self.get_remote_urls()

        async with ClientSession() as client:
            tasks = [self.load_data_from_remote(client, url) for url in urls]
            await asyncio.gather(*tasks)

        sorted_result: list = sorted(self.result, key=lambda i: i['id'])
        pprint(f"Final result:")
        pprint(sorted_result)

        return web.Response(body=str(sorted_result))

    # generate remote(by fact, it is the same current local host)
    def get_remote_urls(self) -> list[str]:
        remote_url: URL = self.request.app.router['remote'].url_for()
        return [
            'http://{}{}'.format(
                self.request.host,
                remote_url.with_query('&'.join(f'params={b}' for b in self.BOUNDS[i]))
            )
            for i in range(3)
        ]

    # for checking timeout can be changed
    @set_timeout(timeout=REQUEST_TIMEOUT)
    async def load_data_from_remote(self, client: ClientSession, url: str):
        async with client.get(url) as response:
            await asyncio.sleep(random.randint(1, MAX_RANDOM_TIMEOUT))

            data_block: str = await response.text()
            new_data = json.loads(data_block).get('data')
            self.result.extend(new_data)

            pprint(f"New data from url: {url}")
            await response.release()
