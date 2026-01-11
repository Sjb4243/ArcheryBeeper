import pygame
from src.pyinit.handle_keydown import handle_keydown
import time
#Could maybe separate this class out to have a base action then action with a countdown to account for collect
#Seems like a lot of work for relatively little payoff atm
class Action:
    def __init__(self, typeof, countdown, beeps, change_detail = False):
        self.type = typeof
        self.countdown = countdown
        self.beeps = beeps
        self.change_detail = change_detail
        self.has_changed = False


    def start(self, appstate):
        #User feedback
        appstate.skip = False
        print(f"Entering {self.type}")
        #Start the countdown that we instantiated action with
        appstate.play_sound(self.beeps)
        self.countdown.start_countdown(appstate, type=self.type)
        #If change detail is True and its not already changed then we want to change it
        #if we hit exit, we want to go back to main menu
        if appstate.exit:
            return
        if not self.has_changed and self.change_detail:
            appstate.change_detail()
            self.has_changed = True
        #If the pause key was pressed, changing appstate.pause then we enter the pause loop
        if appstate.pause == True:
            self.pause(appstate)
        #if we have skipped do nothing (cntinues to next iteration in queue)
        if appstate.skip:
            pass
        time.sleep(0.2)


    def pause(self, appstate):
        ready = False
        print("helo")
        appstate.update_state("pause")
        while not ready:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    handle_keydown(event, appstate.pause_keys)
                    #if we have chosen to skip we set ready to be true
                    if appstate.exit:
                        appstate.pause = False
                        return
                    ready = appstate.skip
        appstate.pause = False
