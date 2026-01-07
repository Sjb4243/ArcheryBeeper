import pygame
from handle_keydown import handle_keydown
class Action:
    def __init__(self, typeof, countdown, beeps, change_detail = False):
        self.type = typeof
        self.countdown = countdown
        self.beeps = beeps
        self.change_detail = change_detail
        self.has_changed = False


    def start(self, appstate):
        print(f"Entering {self.type}")
        appstate.play_sound(self.beeps)
        state = self.countdown.start_countdown(appstate, type=self.type)
        if not self.has_changed and self.change_detail:
            appstate.change_detail()
            self.has_changed = True
        if appstate.pause == True:
            self.pause()
            appstate.pause = False
        if state == "exit":
            return "exit"

    def pause(self):
        from maps import pause_keys
        ready = False
        while not ready:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    skip = handle_keydown(event, pause_keys)
                    ready = skip