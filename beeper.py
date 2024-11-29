import pygame
import time
import sys
import math
import os

#TODO set up a routine class that takes in functions and runs through them, allows for customisation


#Object for drawing text on the screen, nothing much of note
#Main thing is translating strings into actual positions for text in __get_pos__
class label:
    def __init__(self, text, pos, size, colour = (255, 255, 255)):
        self.text = text
        self.init_pos = pos
        self.size = size
        self.colour = colour
        self.font_init = pygame.font.SysFont('Arial', self.size)
        self.render = self.font_init.render(str(f"{self.text}"), True, self.colour)
        self.pos = self.__get_pos__()


    def display(self):
        screen.blit(self.render, self.pos)

    def __get_pos__(self):
        if self.init_pos == "bottom left":
            display_x = 10
            display_y = screen_height - self.render.get_height()
        if self.init_pos == "top right":
            display_x= screen_width - self.render.get_width()
            display_y = 10
        if self.init_pos == "center":
            display_x, display_y, dummy1, dummy2 = self.render.get_rect(center=(screen_width // 2, screen_height // 2))

        return (display_x, display_y)



def get_max_font_size(text):
    screen_width, screen_height = screen.get_size()
    max_font_size = 10
    increment = 5
    while True:
        font = pygame.font.SysFont('Arial', max_font_size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_width, text_height = text_surface.get_size()
        # Check if the text is too large for the screen
        if text_width > screen_width or text_height > screen_height:
            break
        max_font_size += increment
    #Reduce font size
    return max_font_size - increment - 10

def change_current_detail():
    global detail
    print(f"Next detail: {detail}")
    #Switch the current detail to the opposite one
    detail = "CD" if detail == "AB" else "AB"

def shoot(sound, final = False):
    global detail
    #Get to waiting line, 2 beeps
    play_sound(sound, 2, 0.5)
    #This is to track seconds
    start_ticks = pygame.time.get_ticks()
    #Start the countdown, if it returns false (escape was pressed) go backl to main menu after swapping detail
    exited = countdown(start_ticks, 10, "walking")
    if not exited:
        time.sleep(1)
        screen.fill(GREEN_COLOUR)
        #Start shooting beep
        play_sound(sound, 1, 0.5)
        #Same thing as before, but 120 seconds
        start_ticks = pygame.time.get_ticks()
        countdown(start_ticks, 120, "shooting")
    if not final:
        change_current_detail()
    else:
        pygame.event.clear()
        return False



def countdown(start, length, type = None):
    done = False
    #Allow for pressing escape mid countdown
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen.fill(DEFAULT_COLOUR)
                    pygame.display.update()
                    pygame.event.clear()
                    done = True
                    return True
                elif event.key == pygame.K_ESCAPE:
                    main(detail)
                    return True

        screen.fill(DEFAULT_COLOUR)
        #Get the amount of seconds that have passed
        seconds = (pygame.time.get_ticks() - start) / 1000
        if length - int(seconds) > 0:
        #Convert to int, and display
            display_number = length - int(seconds)
        else:
            display_number = 0
        #Orange if shooting + <30 seconds left, green if shooting, red otherwise
        screen.fill(ORANGE_COLOUR if type == "shooting" and display_number <= 30 else GREEN_COLOUR if type == "shooting" else DEFAULT_COLOUR)

        #Mostly font stuff, this is the thing that may need tweaking on new displays
        #Display for seconds
        time_remaining = label(str(f"{display_number}"), "top right", large_font_size)
        time_remaining.display()

        #Display for detail
        detail_text = label(str(f"{detail}"), "bottom left", small_font_size)
        detail_text.display()


        pygame.display.update()
        #If display number is zero, then we're done
        if display_number == 0:
            done = True

    screen.fill(DEFAULT_COLOUR)
    pygame.display.update()
    pygame.event.clear()
    return False

def play_sound(sound, times, delay):
    #Loop through however many times you want the sound to play, play it and then start a delay
    for _ in range(times):
        sound.play()
        time.sleep(delay)

def collect(sound):
    next_detail_text = label(str(f"Next:{detail}"), "center", 400)
    next_detail_text.display()
    pygame.display.update()
    play_sound(sound, 3, 0.5)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen.fill(DEFAULT_COLOUR)
                    pygame.display.update()
                    pygame.event.clear()
                    done = True


def handle_keydown(event, queue, sound, detail):
    if event.key == pygame.K_r:
        process_queue(queue)
    elif event.key == pygame.K_1:
        shoot(sound)
    elif event.key == pygame.K_c:
        collect(sound)
    elif event.key == pygame.K_d:
        change_current_detail()
    elif event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()

def process_queue(queue):
    shot_already = False
    for idx, (process, args) in enumerate(queue):
        process(*args)
        if idx < len(queue) - 1:
            if queue[idx][0].__name__ == "shoot":
                print(f"Press space to continue to next process: {queue[idx + 1][0].__name__}(final)")
            else:
                print(f"Press space to continue to next process: {queue[idx + 1][0].__name__}")
            wait_for_space()
        else:
            print(f"Main menu \n Press r for a full run \n press 1 for a single run \n press d to change detail ")
            return False

def wait_for_space():
    ready = False
    while not ready:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ready = True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main(init):
    global detail
    detail = init
    print(f"Main menu \n Press r for a full run \n press 1 for a single run \n press d to change detail ")
    pygame.event.clear()
    print(f"Next detail: {detail}")
    screen.fill(DEFAULT_COLOUR)
    pygame.display.update()
    mp3 = [file for file in os.listdir(os.path.dirname(os.path.abspath(sys.argv[0]))) if file.endswith("mp3")][0]
    sound = pygame.mixer.Sound(mp3)
    queue = [
        (shoot, (sound,)),  # Function and single argument
        (shoot, (sound, True)),  # Function with two positional arguments, 'True' for final
        (collect, (sound,)),  # Function and single argument
    ]
    #Get the maximum allowed font size for the seconds, the detail size is a percentage of thhis
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                handle_keydown(event, queue, sound, detail)

pygame.init()
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
DEFAULT_COLOUR = (220, 20, 60)
GREEN_COLOUR = (50, 205, 50)
ORANGE_COLOUR = (255, 140, 0)
large_font_size = get_max_font_size("B120")
small_font_size = math.floor(large_font_size * 0.50)
# Set to 30 FPS
pygame.time.Clock().tick(30)

print("\nINSTRUCTIONS")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Press 1 to start shooting process 1 time")
print("Press 2 to start shooting process 2 times")
print("Press c to start collecting process")
print("Press d to change detail")
print("Press ESC to exit whichever process you are in")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
main("AB")