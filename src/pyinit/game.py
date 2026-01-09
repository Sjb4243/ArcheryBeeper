import time
import sys
import math
import os
import pygame
from src.pyinit.ActionQueue import ActionQueue
from src.pyinit.Countdown import Countdown
from src.pyinit.Action import Action
from src.pyinit.Label import Label
from src.pyinit.handle_keydown import handle_keydown
from src.pyinit.maps import generate_keymaps
#Screen object for calculating a lot of font sizes
#Also has some wrapper methods to make calling them a bit easier
class Screen:
    def __init__(self):
        self.screen, self.screenheight, self.screenwidth = self._generate_screen()
        self.max_font_size = self._calc_max_front_size()
        self.small_font_size = math.floor(self.max_font_size * 0.50)



    def _generate_screen(self):
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        screen = pygame.display.set_mode((screen_width, screen_height))
        return screen, screen_height, screen_width

    def _calc_max_front_size(self):
        #Just a random bit of text to calculate with
        text = "B120"
        max_font_size = 10
        increment = 5
        while True:
            font = pygame.font.SysFont('Arial', max_font_size)
            text_surface = font.render(text, True, (255, 255, 255))
            text_width, text_height = text_surface.get_size()
            # Check if the text is too large for the screen
            if text_width > self.screenwidth or text_height > self.screenheight:
                break
            max_font_size += increment
        # Reduce font size
        return max_font_size - increment - 10

    #Wrapper methods for calling
    def display_label(self, label):
        self.screen.blit(label.render, label.pos)

    def fill(self, colour):
        self.screen.fill(colour)



#Appstate is a class to carry around a lot of the essential but boring information about the program's current state
#Also has some methods to change info
class Appstate:
    def __init__(self, screen, pygame_to_tkcomm):
        self.screen = screen
        self.colours = {
            "red":(220, 20, 60),
            "green":(50, 205, 50),
            "orange":(255, 140, 0)
        }
        self.curr_detail = "AB"
        self.main_menu_keys = None
        self.countdown_keys = None
        self.pause_keys = None
        self.sound = pygame.mixer.Sound([file for file in os.listdir(os.path.dirname(os.path.abspath(sys.argv[0]))) if file.endswith("mp3")][0])
        self.state = "main_menu"
        self.pause = False
        self.exit = False
        self.skip = False
        self.pygame_to_tkcomm = pygame_to_tkcomm

    def play_sound(self, times, delay=0.5):
        for _ in range(times):
            self.sound.play()
            time.sleep(delay)

    def change_detail(self):
        self.curr_detail = "AB" if self.curr_detail == "CD" else "CD"

    def change_and_display_detail(self):
        self.screen.fill("red")
        self.change_detail()
        print(f"Next detail {self.curr_detail}")
        next_detail_text = Label(str(f"Next:{self.curr_detail}"), "center", 400, self.screen)
        self.screen.display_label(next_detail_text)
        pygame.display.update()
    def update_state(self, newstate):
        self.state = newstate
        self.pygame_to_tkcomm.put(self.state)


#Initialises everything then calls main menu
def start_pygame(pygame_to_tkcomm):
    pygame.init()
    pygame.time.Clock().tick(30)
    screen = Screen()
    appstate = Appstate(screen, pygame_to_tkcomm)
    appstate.main_menu_keys, appstate.countdown_keys, appstate.pause_keys = generate_keymaps(appstate, ActionQueue, Action, Countdown)
    main_menu(appstate)

def main_menu(appstate):
    printed = False
    next_detail_text = Label(str(f"Next:{appstate.curr_detail}"), "center", 400, appstate.screen)
    appstate.screen.display_label(next_detail_text)
    while True:
        if not printed:
            print("Main menu")
            print(f"Next detail: {appstate.curr_detail}")
            printed = True
            appstate.update_state("main_menu")
        appstate.screen.fill("red")
        next_detail_text = Label(str(f"Next:{appstate.curr_detail}"), "center", 400, appstate.screen)
        appstate.screen.display_label(next_detail_text)
        pygame.display.update()

        for event in pygame.event.get():
            #If the result from state is None (key press not mapped, we want to act like its our first time in the menu)
            if event.type == pygame.KEYDOWN:
                state = handle_keydown(event, appstate.main_menu_keys)
                if state == None:
                    printed = False
                    appstate.exit = False
                    appstate.skip = False



