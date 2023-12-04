from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import (
    get_swagger_ui_html,
)
from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
)
from enum import Enum
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # print("TODO#on_startup ...")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return RedirectResponse("/docs")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/docs",
        title=app.title + " - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
    )


@app.get("/probes/live")
async def probes_live():
    return {"now": datetime.now()}


@app.get("/api/v1/topics")
async def get_topic():
    return {"message": "TODO#GET topics"}


class Payload(BaseModel):
    bar: int = Field(1, title="Optional Bar")


class ListTopicsResult(BaseModel):
    # topics: str = Field(..., title="Result Foo")
    foo: str = Field(..., title="Result Foo")
    bar: int = Field(..., title="Result Bar")


# @app.post("/foo/{foo}", response_model=RetModel)
# async def handle_foo(foo: str, payload: Payload):
#     return RetModel(foo=foo, bar=payload.bar)


@app.get("/api/v1/topics/{topic}", response_model=ListTopicsResult)
async def list_topics():
    return ListTopicsResult(foo="foo", bar=1)


@app.post("/api/v1/topics")
async def create_topic():
    return {"message": "TODO#POST topics"}


@app.delete("/api/v1/topics")
async def delete_topic():
    return {"message": "TODO#DELETE topics"}


@app.get("/api/v1/records")
async def list_records():
    return {"message": "TODO#GET topics"}


class BrokerStorage(str, Enum):
    local = "local"
    gcs = "gcs"


class BrokerSettings(BaseSettings):
    storage: BrokerStorage
    bucket: Path
    host: str
    port: int
    log_level: str


def run(settings: BrokerSettings):
    uvicorn.run(
        app, host=settings.host, port=settings.port, log_level=settings.log_level
    )
