from collections import namedtuple, deque
from enum import IntEnum
from threading import Lock

should_exit = False
should_exit_lock = Lock()


def close():
    global should_exit
    should_exit_lock.acquire()
    should_exit = True
    should_exit_lock.release()


def should_close():
    global should_exit
    should_exit_lock.acquire()
    ret = should_exit
    should_exit_lock.release()
    return ret


class InputState(IntEnum):
    INACTIVE = 0
    HOVER = 1
    CLICK = 2


PtrState = namedtuple("PtrState", "ptr_left, ptr_right")
ptr_state = None
ptr_state_lock = Lock()


def submit_ptr_state(_gui_state):
    global ptr_state
    ptr_state_lock.acquire()
    ptr_state = _gui_state
    ptr_state_lock.release()


def get_ptr_state():
    global ptr_state
    ptr_state_lock.acquire()
    ret = ptr_state
    ptr_state_lock.release()
    return ret


gui_clicks = deque()