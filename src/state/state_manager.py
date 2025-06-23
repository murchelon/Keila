import threading
from bib.uteis import log_term


from enum import Enum

class state_type(Enum):
    INIT = 0
    READY = 1
    RUNNING = 2
    CANCELING = 3

class StateManager:
    def __init__(self):
        self._state = state_type.INIT
        self._lock = threading.Lock()

    def set_state(self, new_state: state_type):
        with self._lock:
            self._state = new_state
            log_term(f"[State] New State: {new_state.name}", "GREEN")

    def get_state(self):
        with self._lock:
            return self._state.name