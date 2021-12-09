from flask import Flask
from flask_restful import Api

# from flask_cors import CORS

import sys
from ..resources import workflows


def main():
    app = Flask(__name__)
    # cors = CORS(app)
    app.config["CORS_HEADERS"] = "Content-Type"
    api = Api(app)

    # Actually setup the Api resource routing here
    api.add_resource(workflows.Workflows, "/workflows")
    api.add_resource(workflows.Workflow, "/workflow/<workflow_id>")

    app.run()


if __name__ == "__main__":
    sys.exit(main())
