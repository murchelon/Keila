import threading

class ThreadManager:
    def __init__(self):
        self.threads = {}
        self.lock = threading.Lock()

    def start_thread(self, name, target, args=()):
        stop_event = threading.Event()
        thread = threading.Thread(
            target=self._wrap_target,
            args=(name, target, stop_event) + args,
            daemon=True
        )
        with self.lock:
            self.threads[name] = {"thread": thread, "stop_event": stop_event}
        thread.start()
        return thread

    def _wrap_target(self, name, target, stop_event, *args):
        try:
            target(stop_event, *args)
        finally:
            with self.lock:
                if name in self.threads:
                    del self.threads[name]

    def stop_thread(self, name):
        with self.lock:
            if name in self.threads:
                self.threads[name]["stop_event"].set()

    def stop_all(self):
        with self.lock:
            for info in self.threads.values():
                info["stop_event"].set()

    def is_running(self, name):
        with self.lock:
            return name in self.threads and self.threads[name]["thread"].is_alive()
