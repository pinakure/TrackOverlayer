import time
from threading      import Thread, Event
from getkey         import getkey, keys

class SafeInput:
    def __init__(self, handler) -> None:
        self.thread = None
        self.closed  = Event()
        self.handler= handler

    def start(self):
        self.thread = Thread(target=self.check)  # check if out of focused window in a thread
        self.closed.clear()
        self.thread.start()
        
    def close(self):
        self.closed.set()

    def check(self):
        while not self.closed.isSet():
            key = getkey()
            self.handler(key)
            time.sleep(0.1)
            