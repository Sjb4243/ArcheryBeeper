from Queue import Queue
from Action import Action
import pygame

countdown_keys = {
    pygame.K_SPACE: lambda: "skip",
    pygame.K_p: lambda: "pause",
    pygame.K_ESCAPE: lambda: "exit"
}
pause_keys = {
    pygame.K_SPACE: lambda: "skip",
    pygame.K_ESCAPE: lambda: "exit",
}

def make_main_menu_keys(appstate):
    from Countdown import Countdown
    walking_count = Countdown(5)
    shooting_count = Countdown(10)
    collect_count = Countdown(0)
    walking_action = Action("walking", walking_count, 2)
    shooting_action = Action("shooting", shooting_count, 1, True)
    collect_action = Action("collecting", collect_count, 3)
    return {
        pygame.K_d: lambda: appstate.change_and_display_detail(),
        pygame.K_f: Queue(appstate,walking_action, shooting_action, walking_action, shooting_action, collect_action),
        pygame.K_1: Queue(appstate, walking_action, shooting_action),
        pygame.K_c: Queue(appstate, collect_action)
    }