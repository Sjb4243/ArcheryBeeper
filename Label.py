import pygame

class Label:
    def __init__(self, text, pos, size,screen, colour = (255, 255, 255)):
        self.text = text
        self.init_pos = pos
        self.size = size
        self.colour = colour
        self.font_init = pygame.font.SysFont('Arial', self.size)
        self.render = self.font_init.render(str(f"{self.text}"), True, self.colour)
        self.pos = self.__get_pos__(screen)


    def __get_pos__(self, screen):
        if self.init_pos == "bottom left":
            display_x = 10
            display_y = screen.screenheight - self.render.get_height()
        elif self.init_pos == "top right":
            display_x= screen.screenwidth - self.render.get_width()
            display_y = 10
        elif self.init_pos == "center":
            display_x, display_y, dummy1, dummy2 = self.render.get_rect(center=(screen.screenwidth // 2, screen.screenheight // 2))

        return (display_x, display_y)