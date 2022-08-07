import threading
from typing import Callable, TypeVar, Tuple


class NoFreeWorkerError(Exception):
    pass


T = TypeVar('T')


class Worker:
    def __init__(self, num_worker: int, creation_func: Callable[[], T]):
        self._worker = [creation_func() for _ in range(num_worker)]
        self._worker_lock = [0] * num_worker
        self._lock = threading.Lock()

    @property
    def count(self):
        return len(self._worker)

    def acquire(self) -> Tuple[int, T]:
        self._lock.acquire()
        try:
            idx = self._worker_lock.index(0)
            self._worker_lock[idx] = 1
            return idx, self._worker[idx]
        except ValueError:
            raise NoFreeWorkerError()
        finally:
            self._lock.release()

    def release(self, idx: int):
        self._lock.acquire()
        self._worker_lock[idx] = 0
        self._lock.release()

    def release_all(self):
        self._lock.acquire()
        self._worker_lock = [0] * len(self._worker)
        self._lock.release()
