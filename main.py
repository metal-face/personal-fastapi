#!/usr/bin/env python3
from fastapi import FastAPI
from databases import Database
from server.utils import services
from server.api.rest.v1.accounts import router
from server.utils import settings
from server.adapters import database
from aioredis import Redis

import uvicorn

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def start_database():
    services.database = Database(
        database.dsn(
            driver=settings.DB_DRIVER,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
        ),
    )
    await services.database.connect()


@app.on_event("shutdown")
async def stop_database():
    await services.database.disconnect()


@app.on_event("startup")
async def start_redis():
    services.redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
    )
    await services.redis.initialize()


@app.on_event("shutdown")
async def stop_redis():
    await services.redis.close()


if __name__ == "__main__":
    uvicorn.run("main:app")
