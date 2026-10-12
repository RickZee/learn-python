from pathlib import Path

from fastapi import FastAPI


def create_app(database: Path) -> FastAPI:
    raise NotImplementedError
