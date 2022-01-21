import os
import json
import flask
from flask import request
from flask_restful import reqparse, Resource
from ewokscore import execute_graph


class Execute(Resource):
    def post(self):
        print("Submit workflow execution:", request.json)
        load_options = {"root_dir": os.getcwd()}
        flask.g.workers.submit(execute_graph, request.json, load_options)
        return request.json, 200


class Workflows(Resource):
    def get(self):
        allWorkflows = []
        print("Current Working Directory ", os.getcwd())
        with os.scandir(path="./workflows") as it:
            for entry in it:
                if not entry.name.startswith(".") and entry.is_file():
                    # print(entry.name)
                    allWorkflows.append(entry.name)
        return allWorkflows

    def post(self):
        print(request.json["graph"])
        # serch for file name=id and IF NOT EXITS create using the request.json
        # if name=id exists return error "workflow exists! Please change name and retry."
        with os.scandir(path="./workflows") as it:
            for entry in it:
                print(entry.name)
                if entry.name == request.json["graph"]["id"] or entry.name == request.json["graph"]["id"] + '.json':
                    return "Workflow exists! Please change name and retry.", 400
        # fdopen(fd, *args, **kwargs)
        f = open(f"./workflows/{request.json['graph']['id'] + '.json'}", "w")
        f.write(json.dumps(request.json, indent=2))
        f.close()
        return request.json, 200


class Workflow(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Workflow, self).__init__()

    def get(self, workflow_id):
        print(workflow_id)
        with os.scandir(path="./workflows") as it:
            for entry in it:
                if (
                    not entry.name.startswith(".")
                    and entry.is_file()
                    and (entry.name == workflow_id + '.json' or entry.name == workflow_id)
                ):
                    print(entry.name)
                    try:
                        fp = open(entry)
                    except PermissionError:
                        return "some default data"
                    else:
                        with fp:
                            return json.loads(fp.read())

    def put(self, workflow_id):
        print(workflow_id)
        # search for file name=id and update with the incoming json
        # if no file exists then save like a post with id=label and warn
        # that a new file was created.
        with os.scandir(path="./workflows") as it:
            for entry in it:
                # print(entry.name)
                if entry.name == workflow_id + '.json' or entry.name == workflow_id:
                    f = open(f"./workflows/{entry.name}", "w")
                    print("found it", entry.name)
                    f.write(json.dumps(request.json, indent=2))
                    f.close()
                    break
        return workflow_id, 200

    def delete(self, workflow_id):
        print(workflow_id)
        # File name
        file = workflow_id
        # File location
        location = "./workflows"
        # Path
        path = os.path.join(location, file)
        # Remove the file
        os.remove(path)
        print("%s has been removed successfully" % file)
        return workflow_id, 200
