from .router import router as _router
from .socketio import create_socketio_app as _create_socketio_app

routers = {(1, 0, 0): _router}

app_creators = {(1, 0, 0): _create_socketio_app}
