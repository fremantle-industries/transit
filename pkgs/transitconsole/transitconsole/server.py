from fastapi import FastAPI
from pydantic_settings import (
    BaseSettings,
)
import uvicorn


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "TODO#GET /home"}


class ConsoleSettings(BaseSettings):
    host: str
    port: int
    log_level: str


def run(settings: ConsoleSettings):
    uvicorn.run(
        app, host=settings.host, port=settings.port, log_level=settings.log_level
    )
