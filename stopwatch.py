import time


class Stopwatch:
    _start = None

    def start(self):
        self._start = time.time()

    def stop(self):
        measured_time = time.time() - self._start
        self._start = None
        return measured_time

    def pause(self, data):
        time.sleep(data)
