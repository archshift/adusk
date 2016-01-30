from threading import Lock

should_exit = False
should_exit_lock = Lock()


def close():
    global should_exit
    with should_exit_lock:
        should_exit = True


def should_close():
    global should_exit
    with should_exit_lock:
        ret = should_exit
    return ret
