from tkinter import ttk
import tkinter as tk
import pygame
class Buttongroup:
    def __init__(self, buttons):
        self.buttons = buttons

    def update_buttons(self):
        for button in self.buttons:
            container = button.container
            if container.winfo_manager():
                container.pack_forget()
            else:
                container.pack(fill="x", pady=3)
            button.regenerate_self()
        container.master.update_idletasks()
            
class Keybutton(ttk.Checkbutton):
    def __init__(self, root, text, key):
        self.container = ttk.Frame(root, padding=5)
        self.inactive_duration = 800
        self.root = root
        self.style = 'Toggle.TButton'
        self.var = tk.BooleanVar(value=False)
        super().__init__(
            self.container,
            text=text,
            style=self.style,
            command=self.clicked,
            variable=self.var
        )

        self.pack(fill="x")

        self.originaltext = text
        self.key = key

    def regenerate_self(self):
        self.config(text=self.originaltext)
        self.var.set(False)

    def _inject_key(self):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=self.key))

    def _disable_self(self):
        self.config(state = "disabled")
        self.root.after(self.inactive_duration, lambda: self.config(state="enabled"))
    def clicked(self):
        self._inject_key()
        self._disable_self()

        
class Pausekeybutton(Keybutton):
    def __init__(self, root, text, key):
        super().__init__(root, text=text, key=key)
        self.inactive_duration = 200
    def clicked(self):
        if self.cget("text") == self.originaltext:
            self.config(text="Pause requested")
        else:
            self.config(text = self.originaltext)
        self._inject_key()
        self._disable_self()

def generate_buttons(root):

    button_map = {
        "main_menu": Buttongroup([
            Keybutton(root, text="Full run",
                      key=pygame.K_f),

            Keybutton(root, text="Change detail",
                      key=pygame.K_d),

            Keybutton(root, text="One run",
                      key=pygame.K_1),

            Keybutton(root, text="Collect",
                      key=pygame.K_c),

            Keybutton(root, text="Quit",
                      key=pygame.K_ESCAPE)
        ]),

        "countdown": Buttongroup([
            Keybutton(root, text="Next",
                      key=pygame.K_SPACE),
            Pausekeybutton(root, text="Pause",
                      key=pygame.K_p),

            Keybutton(root, text="Main menu",
                      key=pygame.K_ESCAPE)
        ]),

        "pause": Buttongroup([
            Keybutton(root, text="Unpause",
                      key=pygame.K_SPACE),

            Keybutton(root, text="Main menu",
                      key=pygame.K_ESCAPE)
        ]),
    }

    return button_map

