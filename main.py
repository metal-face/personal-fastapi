from fastapi import FastAPI
from databases import Database
import settings
import adapters.database

app = FastAPI()

@app.on_event("startup")
async def start_database():
    app.state.database = Database(
        adapters.database.dsn(
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