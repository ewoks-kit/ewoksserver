import time
from flask_socketio import SocketIO, emit


def connected():
    print("Connected")


def disconnected():
    print("Disconnected")


def execute(graph):
    print("Execute Graph")
    print(graph)

    executingEvents = [
        {
            "id": "1",
            "nodeId": "Prepare test set grid data",
            "event_type": "start",
            "values": {"a": 1, "b": 2},
            "executing": ["Prepare test set grid data"],
        },
        {
            "id": "2",
            "nodeId": "Prepare test set grid data",
            "event_type": "stop",
            "values": {"a": 1, "b": 2, "c": 3},
            "executing": [""],
        },
        {
            "id": "3",
            "nodeId": "EstTask_1",
            "event_type": "start",
            "values": {"a": 1, "b": 2, "c": 3, "d": 4},
            "executing": ["EstTask_1"],
        },
        {
            "id": "4",
            "nodeId": "CommonPrepareExperiment",
            "event_type": "start",
            "values": {"a": 1, "b": 2},
            "executing": ["CommonPrepareExperiment", "EstTask_1"],
        },
        {
            "id": "5",
            "nodeId": "EstTask_1",
            "event_type": "stop",
            "values": {"a": 1, "b": 2, "c": 3, "d": 4},
            "executing": ["CommonPrepareExperiment"],
        },
        {
            "id": "6",
            "nodeId": "EstTask_0",
            "event_type": "start",
            "values": {"a": 1, "b": 2, "c": 3, "d": 4},
            "executing": ["EstTask_0", "CommonPrepareExperiment"],
        },
        {
            "id": "7",
            "nodeId": "CommonPrepareExperiment",
            "event_type": "stop",
            "values": {"a": 1, "b": 2},
            "executing": ["EstTask_0"],
        },
        {
            "id": "8",
            "nodeId": "Read and set grid data",
            "event_type": "start",
            "values": {"a": 1, "b": 2, "c": 3, "d": 4},
            "executing": ["EstTask_0", "Read and set grid data"],
        },
        {
            "id": "9",
            "nodeId": "EstTask_0",
            "event_type": "stop",
            "values": {"a": 1, "b": 2, "c": 3, "d": 4},
            "executing": ["Read and set grid data"],
        },
        {
            "id": "10",
            "nodeId": "Read and set grid data",
            "event_type": "stop",
            "values": {"a": 1, "b": 2, "c": 3, "d": 4},
            "executing": [""],
        },
        {
            "id": "11",
            "nodeId": "Prepare test set grid data",
            "event_type": "start",
            "values": {"a": 1, "b": 2},
            "executing": ["Prepare test set grid data"],
        },
        {
            "id": "12",
            "nodeId": "Prepare test set grid data",
            "event_type": "stop",
            "values": {"a": 1, "b": 2, "c": 3},
            "executing": [""],
        },
    ]

    for ev in executingEvents:
        print(ev)
        emit("Executing", ev, broadcast=True)
        time.sleep(4)  # * random.seed(float(ev.id))


def add_events(socketio: SocketIO):
    socketio.on("connect")(connected)
    socketio.on("disconnect")(disconnected)
    socketio.on("Execute Graph")(execute)
