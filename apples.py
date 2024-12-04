import pygame
import random
import settings

class Apple:
    def __init__(self, window_width, window_height, update_hook):
        self.window_width = window_width
        self.window_height = window_height
        self.image = pygame.image.load("apple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(pygame.Color(255, 255, 255, 255))
        self.rect = self.image.get_rect()
        self.reset_position()
        self.speed = settings.GRAV
        self.update_hook = update_hook

    def reset_position(self):
        self.rect.x = random.randint(0, self.window_width - self.rect.width)
        self.rect.y = random.randint(-200, -50)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > self.window_height:
            self.reset_position()
            self.update_hook()

    def check_collision(self, player_rect):
        if self.rect.colliderect(player_rect):
            self.reset_position()
            return True  # Collision
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
