
import pygame
import sys
#key mapping

def generate_keymaps(appstate, Queue, Action, Countdown):
    def handle_escape():
        appstate.exit = True
    def handle_space():
        appstate.skip = True

    def handle_pause():
        appstate.pause = False if appstate.pause else True
        pauseonoff = "Pause on" if appstate.pause else "Pause off"
        print(pauseonoff)

    countdown_keys = {
        pygame.K_SPACE: lambda: handle_space(),
        pygame.K_p: lambda: handle_pause(),
        pygame.K_ESCAPE: lambda: handle_escape()
    }

    pause_keys = {
        pygame.K_SPACE: lambda: handle_space(),
        pygame.K_ESCAPE: lambda: handle_escape()
    }
    walking_count = Countdown(5)
    shooting_count = Countdown(10)
    # We just want the beeping, I could have a base action class to avoid a lot of this specific stuff
    collect_count = Countdown(0)
    walking_action = Action("walking", walking_count, 2)
    shooting_action = Action("shooting", shooting_count, 1, True)
    collect_action = Action("collecting", collect_count, 3)
    main_menu_keys =  {
        pygame.K_d: lambda: appstate.change_and_display_detail(),
        pygame.K_f: Queue(appstate, walking_action, shooting_action, walking_action, shooting_action, collect_action),
        pygame.K_1: Queue(appstate, walking_action, shooting_action),
        pygame.K_c: Queue(appstate, collect_action),
        pygame.K_ESCAPE: lambda: sys.exit()
    }
    return main_menu_keys, countdown_keys, pause_keys



