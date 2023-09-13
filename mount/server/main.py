#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from server.utils import services
from server.api.rest.v1.sessions import router as sessions_router
from server.api.rest.v1.accounts import router as accounts_router
from server.api.rest.v1.blogs import router as blogs_router
from server.api.rest.v1.search import router as search_router
from server.utils import settings
from server.adapters import database
from aioredis import Redis

app = FastAPI()
app.include_router(accounts_router)
app.include_router(sessions_router)
app.include_router(blogs_router)
app.include_router(search_router)


origins = [
    "http://localhost:3000",
    "http://localhost:10000",
    "https://metalface.ca",
    "https://metalface.ca/",
    "https://api.metalface.ca",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
