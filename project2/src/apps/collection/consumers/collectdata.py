import asyncio
import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from src.apps.collection.utils import generate_remote_data


class CollectDataConsumer(AsyncJsonWebsocketConsumer):
    bounds = [((1, 11), (31, 41)), ((11, 21), (41, 51)), ((21, 31), (51, 61))]

    async def connect(self) -> None:
        await self.accept()

        self.result = []
        await asyncio.gather(
            self.async_task(1, self.bounds[0]),
            self.async_task(2, self.bounds[1]),
            self.async_task(1, self.bounds[2])
        )

        sorted_result: list = sorted(self.result, key=lambda i: i['id'])

        print('Result:{}'.format(sorted_result))
        await self.send(json.dumps({'data': sorted_result}))

    async def disconnect(self, close_code: int) -> None:
        await self.close(close_code)

    async def async_task(self, delay: int, item: tuple) -> None:
        async for i in generate_remote_data(delay, *item):
            print(f'Curr element:{i}')
            self.result.append(i)

            if len(self.result) % 5 == 0:
                await self.send(text_data='Подгружено: {} элементов.'.format(len(self.result)))
