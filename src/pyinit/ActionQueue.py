import time
#Queue object that just goes through each arg and runs the start method on it
class ActionQueue:
    def __init__(self,appstate,*events):
        self.appstate = appstate
        self.events = events

    def process_events(self):
        for obj in self.events:
            #if escape was ever pressed we want to return to the main menu
            obj.start(self.appstate)
            if self.appstate.exit:
                return
            time.sleep(0.5)



