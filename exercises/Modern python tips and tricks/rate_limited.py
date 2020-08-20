from functools import wraps
import time


def rate_limited(**kwargs):
    per_second = kwargs.pop('per_second')
    assert kwargs == {}
    wait_interval = 1.0 / per_second
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kargs):
            elapsed = time.clock() - wrapper.last_time_called
            if elapsed < wait_interval:
                time.sleep(wait_interval - elapsed)
            return_value = func(*args, **kargs)
            wrapper.last_time_called = time.clock()
            return return_value
        wrapper.last_time_called = 0
        return wrapper
    return decorator


if __name__ == "__main__":
    @rate_limited(per_second=3)
    def greet(name="world"):
        print("Hello {}".format(name))

    greet("Trey")
    greet("Diane")
    greet()
