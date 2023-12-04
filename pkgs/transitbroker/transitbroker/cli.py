import typer
from typing_extensions import Annotated
from pathlib import Path
from transitbroker.server import run, BrokerSettings, BrokerStorage

app = typer.Typer()


@app.command()
def start(
    storage: Annotated[
        BrokerStorage,
        typer.Argument(
            envvar="TRANSIT_BROKER_STORAGE",
            help="storage engine for topics and records",
        ),
    ],
    bucket: Annotated[
        Path,
        typer.Argument(
            envvar="TRANSIT_BROKER_BUCKET", help="bucket to use in storage engine"
        ),
    ],
    host: Annotated[
        str, typer.Argument(envvar="TRANSIT_BROKER_HOST", help="listen on host")
    ] = "0.0.0.0",
    port: Annotated[
        int, typer.Argument(envvar="TRANSIT_BROKER_PORT", help="listen on port")
    ] = 8080,
    log_level: Annotated[
        str, typer.Argument(envvar="TRANSIT_BROKER_LOG_LEVEL", help="log level")
    ] = "info",
):
    settings = BrokerSettings(
        storage=storage,
        bucket=bucket,
        host=host,
        port=port,
        log_level=log_level,
    )
    run(settings)


if __name__ == "__main__":
    app()
