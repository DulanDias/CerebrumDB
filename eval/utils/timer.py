import time
from contextlib import contextmanager

@contextmanager
def measure_latency():
    start = time.time()
    yield
    end = time.time()
    print(f"Latency: {(end - start) * 1000:.2f} ms")
