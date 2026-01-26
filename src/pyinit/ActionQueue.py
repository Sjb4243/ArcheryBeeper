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
                break
            time.sleep(0.5)
        #fix for bug where after one run the details dont change properly
        for obj in self.events:
            obj.has_changed = False



