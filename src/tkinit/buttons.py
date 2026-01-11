from tkinter import ttk
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

        self.style = 'Toggle.TButton'
        super().__init__(
            self.container,
            text=text,
            style=self.style,
            command=self.clicked
        )

        self.pack(fill="x")

        self.originaltext = text
        self.key = key

    def regenerate_self(self):
        self.config(text=self.originaltext)
        self.state(["!selected"])
        
    def _inject_key(self):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=self.key))
        
    def clicked(self):
        self._inject_key()
        
        
class Pausekeybutton(Keybutton):
    def __init__(self, root, text, key):
        super().__init__(root, text=text, key=key)

    def clicked(self):
        if self.cget("text") == self.originaltext:
            self.config(text="Pause requested")
        else:
            self.config(text = self.originaltext)
        self._inject_key()

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
            Keybutton(root, text="Next",
                      key=pygame.K_SPACE),

            Keybutton(root, text="Main menu",
                      key=pygame.K_ESCAPE)
        ]),
    }

    return button_map

