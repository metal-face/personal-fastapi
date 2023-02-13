from fastapi import FastAPI
from databases import Database
from server.controllers.accounts import router
from server import settings
from server.adapters import database

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def start_database():
    app.state.database = Database(
        database.dsn(
            driver=settings.DB_DRIVER,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
        ),
    )
    await app.state.database.connect()


@app.on_event("shutdown")
async def stop_database():
    await app.state.database.disconnect()
