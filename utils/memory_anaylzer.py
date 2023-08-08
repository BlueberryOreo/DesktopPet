import psutil
import os

pid = os.getpid()
p = psutil.Process(pid)

def memory_analyze(func):
    def wrapper(*args, **kwargs):
        print(f"[DEBUG] process memory before function {func.__name__} called: {get_current_memory()}")
        ret = func(*args, **kwargs)
        print(f"[DEBUG] process memory after function {func.__name__} called: {get_current_memory()}")
        return ret
    return wrapper

def get_current_memory():
    global p
    info = p.memory_full_info()
    return info.uss / 1024. / 1024. # MB
