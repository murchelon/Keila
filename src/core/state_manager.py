import threading
from bib.uteis import log_term


from enum import Enum

class State(Enum):
    INIT = 0
    READY = 1
    LISTENING = 2
    RUNNING = 3
    SPEAKING = 4
    CANCELING = 5

class StateManager:
    def __init__(self):
        self._state = State.INIT
        self._lock = threading.Lock()

    def set_state(self, new_state: State):
        with self._lock:
            self._state = new_state
            log_term(f"[State] New State: {new_state.name}", "GREEN")

    def get_state(self):
        with self._lock:
            return self._state.name