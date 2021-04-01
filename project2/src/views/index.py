import asyncio
import json

from aiohttp import web, ClientSession
from yarl import URL

from src.utils import set_timeout


class IndexView(web.View):
    bounds = [(1, 11, 31, 41), (11, 21, 41, 51), (21, 31, 51, 61)]

    async def get(self) -> web.Response:
        self.result = []
        urls: list = self.get_remote_urls()

        async with ClientSession() as client:
            tasks = [self.load_data_from_remote(client, url) for url in urls]
            await asyncio.gather(*tasks)

        sorted_result: list = sorted(self.result, key=lambda i: i['id'])
        return web.Response(body=str(sorted_result))

    def get_remote_urls(self) -> list:
        remote_url: URL = self.request.app.router['remote'].url_for()
        return [
            'http://{}{}'.format(
                self.request.host,
                remote_url.with_query('&'.join(f'params={b}' for b in self.bounds[i])))
            for i in range(3)
        ]

    @set_timeout(delay=2)
    async def load_data_from_remote(self, client: ClientSession, url: str):
        async with client.get(url) as response:
            data_block: str = await response.text()
            self.result.extend(json.loads(data_block).get('data'))

            print(self.result)
            await response.release()
