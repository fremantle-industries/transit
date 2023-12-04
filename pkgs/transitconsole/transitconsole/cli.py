import typer
from typing_extensions import Annotated
from transitconsole.server import run, ConsoleSettings

app = typer.Typer()


@app.command()
def start(
    host: Annotated[
        str, typer.Argument(envvar="TRANSIT_CONSOLE_HOST", help="listen on host")
    ] = "0.0.0.0",
    port: Annotated[
        int, typer.Argument(envvar="TRANSIT_CONSOLE_PORT", help="listen on port")
    ] = 8080,
    log_level: Annotated[
        str, typer.Argument(envvar="TRANSIT_CONSOLE_LOG_LEVEL", help="log level")
    ] = "info",
):
    settings = ConsoleSettings(
        host=host,
        port=port,
        log_level=log_level,
    )
    run(settings)


if __name__ == "__main__":
    app()
