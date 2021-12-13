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
    api.add_resource(workflows.Execute, "/workflow/execute")

    # workflows.append(request.get_json())
    # obj = WorkflowSkeleton(10)
    # print(obj)
    # WorkflowSkeleton.save_object(obj)

    # class WorkflowSkeleton():
    #     def __init__(self, param):
    #         self.param = {"name": param}
    #     def save_object(obj):
    #         try:
    #             with open("data.pickle", "wb") as f:
    #                 pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    #         except Exception as ex:
    #             print("Error during pickling object (Possibly unsupported):", ex)

    # @app.route("/static/<path:path>")
    # def static_dir(path):
    #     return send_from_directory("static", path)

    # remove(path, *, dir_fd=None)
    #     Remove (delete) the file path.

    # mkdir(path, mode=511, *, dir_fd=None)
    #     Create a directory named path with numeric mode mode.

    # @app.route('/workflows')
    # def get_workflows():
    #   return jsonify(workflows)

    # @app.route('/workflows', methods=['POST'])
    # def add_workflows():
    #   workflows.append(request.get_json())
    #   return '', 204

    app.run()


if __name__ == "__main__":
    sys.exit(main())
