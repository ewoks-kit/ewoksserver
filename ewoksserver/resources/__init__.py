import flask
from . import filesystem


def add_resources(app: flask.Flask):
    """Currently only one resource backend is supported: file system"""
    filesystem.add_file_resources(app)
