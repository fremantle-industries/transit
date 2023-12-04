# syntax=docker/dockerfile:1.3

FROM python:3.11.6-bookworm AS deps
WORKDIR /app
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY pyproject.toml pyproject.toml
COPY Makefile Makefile
COPY requirements.txt requirements.txt
COPY pkgs pkgs
RUN make deps/install

FROM python:3.11.6-bookworm AS build-transitbroker
WORKDIR /app
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY --from=deps /opt/venv /opt/venv
COPY pyproject.toml pyproject.toml
COPY Makefile Makefile
COPY pkgs pkgs
RUN make build/transitbroker

FROM debian:bookworm-20231120-slim AS run-transitbroker
WORKDIR /app
COPY --from=build-transitbroker /app/pkgs/transitbroker/dist/transitbroker bin/transitbroker
CMD ["/app/bin/transitbroker"]

FROM python:3.11.6-bookworm AS build-transitconsole
WORKDIR /app
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY --from=deps /opt/venv /opt/venv
COPY pyproject.toml pyproject.toml
COPY Makefile Makefile
COPY pkgs pkgs
RUN make build/transitconsole

FROM debian:bookworm-20231120-slim AS run-transitconsole
WORKDIR /app
COPY --from=build-transitconsole /app/pkgs/transitconsole/dist/transitconsole bin/transitconsole
CMD ["/app/bin/transitconsole"]
