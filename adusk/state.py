import copy
from collections import namedtuple, deque
from enum import IntEnum
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


class InputState(IntEnum):
    INACTIVE = 0
    HOVER = 1
    CLICK = 2

ptrs = None
ptrs_lock = Lock()


def submit_ptr_state(ptr_left, ptr_right):
    global ptrs
    with ptrs_lock:
        ptrs = (ptr_left, ptr_right)


def get_ptr_state():
    global ptrs
    with ptrs_lock:
        ret = copy.deepcopy(ptrs)
    return ret


gui_clicks = deque()
