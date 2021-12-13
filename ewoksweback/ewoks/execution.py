from contextlib import contextmanager
import multiprocessing
from concurrent.futures import ProcessPoolExecutor


@contextmanager
def worker_pool(max_workers=1):
    ctx = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=max_workers, mp_context=ctx) as pool:
        yield pool
