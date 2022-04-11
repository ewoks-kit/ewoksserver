import os
import json
import flask
from flask import request
from flask_restful import reqparse, Resource

class Tasks(Resource):
    def get(self):
        allTasks = []
        print("Current task Directory ", os.getcwd())
        with os.scandir(path="./tasks") as it:
            for entry in it:
                if (
                    not entry.name.startswith(".")
                    and entry.is_file()
                ):
                    print(entry.name)
                    try:
                        fp = open(entry)
                    except PermissionError:
                        return "some default data"
                    else:
                        with fp:
                            allTasks.append(json.loads(fp.read()))

        #         If only the names of tasks are needed           
        #         if not entry.name.startswith(".") and entry.is_file():
        #             print(entry.name)
        #             allTasks.append(entry.name)
        return allTasks

    def post(self):
        print(request.json)
        with os.scandir(path="./tasks") as it:
            for entry in it:
                print(entry.name)
                if entry.name == request.json["task_identifier"]:
                    return "Task exists! Please change name and retry.", 400

        f = open(f"./tasks/{request.json['task_identifier']}", "w")
        f.write(json.dumps(request.json, indent=2))
        f.close()
        return request.json, 200


class Task(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(Task, self).__init__()

    def get(self, task_id):
        print(task_id)
        with os.scandir(path="./tasks") as it:
            for entry in it:
                if (
                    not entry.name.startswith(".")
                    and entry.is_file()
                    and entry.name == task_id
                ):
                    print(entry.name)
                    try:
                        fp = open(entry)
                    except PermissionError:
                        return "some default data"
                    else:
                        with fp:
                            return json.loads(fp.read())

    def put(self, task_id):
        print(task_id, self.reqparse.parse_args(), request.json)
        # search for file name=id and update with the incoming json
        # if no file exists then save like a post with id=label and warn
        # that a new file was created.
        with os.scandir(path="./tasks") as it:
            for entry in it:
                print(entry.name)
                if entry.name == task_id:
                    f = open(f"./tasks/{entry.name}", "w")
                    print("found it", entry.name)
                    f.write(json.dumps(request.json, indent=2))
                    f.close()
                    break
        return task_id, 200

    def delete(self, task_id):
        print(task_id)
        # File name
        file = task_id
        # File location
        location = "./tasks"
        # Path
        path = os.path.join(location, file)
        # Remove the file
        os.remove(path)
        print("%s has been removed successfully" % file)
        return task_id, 200
