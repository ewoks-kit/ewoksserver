from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def enable_cors(app: FastAPI) -> None:
    """Enable Cross-Origin Resource Sharing"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
