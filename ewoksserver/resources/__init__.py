import flask
from . import filesystem


def add_resources(app: flask.Flask):
    """Currently only one resource backend is supported: file system"""

    @app.route("/")
    def home():
        return app.send_static_file("index.html")

    filesystem.add_file_resources(app)
