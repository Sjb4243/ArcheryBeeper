from src.pyinit.game import start_pygame
import threading
from queue import Queue
from src.tkinit.tkwindow import start_tk



def main():
    pygame_to_tk_communication = Queue()
    pygame_thread = threading.Thread(target=start_pygame, args=(pygame_to_tk_communication,))
    tk_thread = threading.Thread(target=start_tk, args=(pygame_to_tk_communication,))
    pygame_thread.start()
    tk_thread.daemon= True
    tk_thread.start()
    pygame_thread.join()


main()