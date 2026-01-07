
#Queue object that just goes through each arg and runs the start method on it
class Queue:
    def __init__(self,appstate,*events):
        self.appstate = appstate
        self.events = events

    def process_events(self):
        for obj in self.events:
            state = obj.start(self.appstate)
            #if escape was ever pressed we want to return to the main menu
            if self.appstate.exit:
                return


