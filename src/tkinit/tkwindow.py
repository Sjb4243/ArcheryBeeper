import tkinter as tk
from src.tkinit.buttons import generate_buttons
from tkinter import ttk
import os

def update_gui(root, pygame_to_tk_comm, button_map):
    # Check if the function has a state attribute yet
    if not hasattr(update_gui, "state"):
        update_gui.state = "main_menu"
        initbuttons = button_map[update_gui.state]
        initbuttons.update_buttons()

    while not pygame_to_tk_comm.empty():
        new_state = pygame_to_tk_comm.get()
        if update_gui.state is not None:
            oldbuttons = button_map[update_gui.state]
            oldbuttons.update_buttons()
            newbuttons = button_map[new_state]
            newbuttons.update_buttons()
        update_gui.state = new_state
        print(f"New state received: {update_gui.state}")

    root.after(50, update_gui, root, pygame_to_tk_comm, button_map)


def start_tk(pygame_to_tk_comm):
    root = tk.Tk()
    style = ttk.Style()
    style.tk.call('source', "tkinit/assets/azure.tcl")
    style.tk.call('set_theme', 'dark')
    root.configure(padx=10, pady=10)
    button_map = generate_buttons(root)
    update_gui(root, pygame_to_tk_comm, button_map)
    root.mainloop()