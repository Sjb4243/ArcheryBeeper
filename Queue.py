import sys
import time
class Queue:
    def __init__(self,appstate,*events):
        self.appstate = appstate
        self.events = events

    def process_events(self):
        for obj in self.events:
            state = obj.start(self.appstate)
            if state == "exit":
                return
            time.sleep(0.5)
        return state

