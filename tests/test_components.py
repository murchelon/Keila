import time
from bib.threadManager import ThreadManager
from state.state_manager import StateManager, state_type


def test_state_manager():
    sm = StateManager()
    sm.set_state(state_type.READY)
    assert sm.get_state() == 'READY'


def worker(stop_event):
    while not stop_event.is_set():
        time.sleep(0.01)


def test_thread_manager_start_and_stop():
    tm = ThreadManager()
    t = tm.start_thread('w', worker)
    assert tm.is_running('w') is True
    tm.stop_thread('w')
    t.join(timeout=0.2)
    assert not tm.is_running('w')
