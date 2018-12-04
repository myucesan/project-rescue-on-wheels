import time


class Timer:
    _start = None

    def start(self):
        self._start = time.time()

    def stop(self):
        measured_time = time.time() - self._start
        self._start = None
        return measured_time

    def pause(self, data):
        time.sleep(data)

    def conditional_pause(self, data, chunks, condition, checkers):
        print(condition)
        for i in range(chunks):
            if condition > checkers[0] and condition < checkers[1]:
                print("Sensor werkt")
                break
            else:
                time.sleep(data/chunks)
