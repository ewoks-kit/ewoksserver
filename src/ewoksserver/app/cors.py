from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def enable_cors(app: FastAPI) -> None:
    """Enable Cross-Origin Resource Sharing"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # Browsers reject `allow_credentials=True` combined with a wildcard
        # origin anyway, and no client uses cookies/credentials with this API.
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def get_cors_options(app: FastAPI) -> dict | None:
    for mw in app.user_middleware:
        if mw.cls is CORSMiddleware:
            return mw.options
