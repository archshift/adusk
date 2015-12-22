from collections import namedtuple
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


GuiState = namedtuple("GuiState", "virtual_kb, ptr_left, ptr_right")
gui_state = None
gui_state_lock = Lock()


def submit_gui_state(_gui_state):
    global gui_state
    gui_state_lock.acquire()
    gui_state = _gui_state
    gui_state_lock.release()


def get_gui_state():
    global gui_state
    gui_state_lock.acquire()
    ret = gui_state
    gui_state_lock.release()
    return ret
