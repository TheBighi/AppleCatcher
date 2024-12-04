import pygame

class Button:

    def __init__(self, screen, event, pos, text, font_file, font_size):
        self.screen = screen
        self.event = event

        self.was_held = False

        font = pygame.font.Font(font_file, font_size)

        self.text_surface = font.render(text, False, (251, 250, 245))
        self.text_rect = self.text_surface.get_rect(center=pos)

        self.button_rect = pygame.rect.Rect(
            self.text_rect.x - 15,
            self.text_rect.y - 15,
            self.text_rect.w + 25,
            self.text_rect.h + 30
        )

    def is_hovered(self):
        mx, my = pygame.mouse.get_pos()
        return ((mx >= self.button_rect.x and mx <= self.button_rect.right) and
                (my >= self.button_rect.y and my <= self.button_rect.bottom))
        
    def check_click(self):
        if self.is_hovered():
            is_held = pygame.mouse.get_pressed(3)[0]

            if self.was_held and not is_held:
                self.was_held = is_held

                # button was clicked
                self.event()
                return

            self.was_held = is_held

    def draw(self):
        self.screen.blit(self.text_surface, self.text_rect)

    def update(self):
        self.check_click()
        self.draw()
        if self.is_hovered():
            pygame.draw.rect(
                self.screen,
                (251, 250, 245),
                self.button_rect,
                width=6
            )
