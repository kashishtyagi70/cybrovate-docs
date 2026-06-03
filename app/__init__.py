"""Cybrovate documentation application package."""

from typing import Any


def __getattr__(name: str) -> Any:
    if name == "app":
        from app.main import app as fastapi_app

        return fastapi_app
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["app"]
