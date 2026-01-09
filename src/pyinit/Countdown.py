from src.pyinit.handle_keydown import handle_keydown
import pygame
from src.pyinit.Label import Label

class Countdown:
    def __init__(self, length):
        self.length = length

    def start_countdown(self, appstate, type=None):
        if self.length == 0:
            return
        appstate.update_state("countdown")
        start = pygame.time.get_ticks()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #keys are capable of interacting with various flags on appstate
                    handle_keydown(event, appstate.countdown_keys)
                    if appstate.skip:
                        return
                    if appstate.exit:
                        return


            seconds = (pygame.time.get_ticks() - start) / 1000
            if self.length - int(seconds) > 0:
            #Convert to int, and display
                display_number = self.length - int(seconds)
            else:
                display_number = 0
            appstate.screen.fill(appstate.colours["orange"] if type == "shooting" and display_number <= self.length * 0.25 else appstate.colours["green"]if type == "shooting" else appstate.colours["red"])
            time_remaining = Label(str(f"{display_number}"), "top right", appstate.screen.max_font_size, appstate.screen)
            detail_text = Label(str(f"{appstate.curr_detail}"), "bottom left", appstate.screen.small_font_size, appstate.screen)
            appstate.screen.display_label(time_remaining)
            appstate.screen.display_label(detail_text)
            pygame.display.update()
            if display_number == 0:
                done = True
        pygame.display.update()