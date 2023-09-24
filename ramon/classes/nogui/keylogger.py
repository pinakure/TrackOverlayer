import pywintypes, time
from threading      import Thread, Event
from pynput         import keyboard
from getkey         import getkey, keys
        
#from win32gui       import GetWindowText, GetForegroundWindow

class KeyLogger:
    def __init__(self) -> None:
        self.is_paused=False  # pause keylog listener
        self.is_closed=False  # stop and close keylog
        self.l=None  # listener
        #self.listened_window=GetWindowText(GetForegroundWindow())  # set listened window name
        self.focused_checker=Thread(target=self.check_focused)  # check if out of focused window in a thread
        self.focused_checker.start()
    
    def start(self):
        # initialize and start listener
        self.l=keyboard.Listener( on_press=self.on_press, on_release=self.on_release)
        self.l.start()

    def close(self):
        # stop and close keylog
        self.is_closed=True
        self.stop()

    def stop(self):
        # stop listener
        self.l.stop()
        self.l.join()
        
    def check_focused(self):
        return True
        while not self.is_closed:
            if GetWindowText(GetForegroundWindow())!=self.listened_window:  # compare now focused window with listened window
                if not self.is_paused:  # if different and not paused, stop listening
                    self.stop()
                    self.is_paused=True
            elif self.is_paused:  # if same but paused, restart listening
                    self.start()
                    self.is_paused=False
            time.sleep(0.1)

class SafeInput:
    def __init__(self, handler) -> None:
        self.thread = None
        self.run    = Event()
        self.handler= handler

    def start(self):
        self.thread = Thread(target=self.check)  # check if out of focused window in a thread
        self.run.set()
        self.thread.start()
        
    def close(self):
        self.run.clear()

    def check(self):
        while self.run.isSet():
            key = getkey()
            self.handler(key)
            