import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        f = func(*args, **kwargs)
        elapsed = time.time() - start
        return [f, elapsed]
    return wrapper
