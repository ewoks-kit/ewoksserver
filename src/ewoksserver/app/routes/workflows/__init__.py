from .router import v1_0_0_router as _v1_0_0_router
from .router import v2_1_0_router as _v2_1_0_router

routers = {
    (1, 0, 0): _v1_0_0_router,
    (1, 1, 0): _v1_0_0_router,
    (2, 0, 0): _v1_0_0_router,
    (2, 1, 0): _v2_1_0_router,
}
