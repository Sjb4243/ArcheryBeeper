import time
import sys
import math
import os
import pygame
from maps import make_main_menu_keys
from Label import Label
from handle_keydown import handle_keydown


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

    def display_label(self, label):
        self.screen.blit(label.render, label.pos)

    def fill(self, colour):
        self.screen.fill(colour)




class Appstate:
    def __init__(self, screen):
        self.screen = screen
        self.colours = {
            "red":(220, 20, 60),
            "green":(50, 205, 50),
            "orange":(255, 140, 0)
        }
        self.curr_detail = "AB"
        self.sound = pygame.mixer.Sound([file for file in os.listdir(os.path.dirname(os.path.abspath(sys.argv[0]))) if file.endswith("mp3")][0])
        self.pause = False

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



def main():
    pygame.init()
    pygame.time.Clock().tick(30)
    screen = Screen()
    appstate = Appstate(screen)
    main_menu(appstate)

def main_menu(appstate):
    running = True
    print("Main menu")
    print(f"Next detail: {appstate.curr_detail}")
    appstate.screen.fill("red")
    main_menu_keys = make_main_menu_keys(appstate)
    next_detail_text = Label(str(f"Next:{appstate.curr_detail}"), "center", 400, appstate.screen)
    appstate.screen.display_label(next_detail_text)
    pygame.display.update()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                handle_keydown(event, main_menu_keys)
                running = False
    main_menu(appstate)

main()