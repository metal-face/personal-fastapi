from databases import Database
from aioredis import Redis
from httpx import AsyncClient

database: Database
redis: Redis
http_client = AsyncClient()
