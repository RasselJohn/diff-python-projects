import os
from uuid import uuid4

from redis import asyncio as aioredis


class ConnectionManager:
    # without 'await'
    _redis = aioredis.from_url(os.environ['REDIS'])

    async def get_session(self, client_id: str) -> str:
        async with self._redis.pipeline(transaction=True) as redis_transaction:
            await redis_transaction.watch(client_id)

            prev_session = await redis_transaction.get(client_id)
            if prev_session is not None:
                print(f'{client_id=} already exists. Old connection will be closed.')

            new_session = str(uuid4())
            await redis_transaction.set(client_id, new_session)

        print(f'Session {new_session=} started.')
        return new_session

    # with transaction
    async def is_active_session(self, client_id, session):
        async with self._redis.pipeline(transaction=True) as redis_transaction:
            await redis_transaction.watch(client_id)
            is_active = await self._is_active_session(redis_transaction, client_id, session)
            return is_active

    # check that curr session is active
    async def _is_active_session(self, redis_transaction, client_id, session):
        actual_session = await redis_transaction.get(client_id)
        return actual_session and actual_session.decode() == session

    async def get_all_sessions(self):
        keys = await self._redis.keys()
        values = await self._redis.mget(keys)  # keys are ordered
        return (' '.join((k.decode(), v.decode())) for k, v in zip(keys, values))

    async def clean(self, client_id, session):
        async with self._redis.pipeline(transaction=True) as redis_transaction:
            await redis_transaction.watch(client_id)

            # if another new session with the same client_id does not exists
            is_active_session: bool = await self._is_active_session(redis_transaction, client_id, session)
            if is_active_session:
                await redis_transaction.delete(client_id)

        print(f'Session for {session=} finished...')
