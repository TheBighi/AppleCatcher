# Example file showing a circle moving on screen
import pygame
from pygame import mixer
from pygame import KEYDOWN
# pygame setup
pygame.init()
window_width = 1280
window_height = 720
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
dt = 0

gravity_acc = pygame.Vector2(0.0, 1.2)
TERMINAL_VEL = 10


apple_img = pygame.image.load("apple.png").convert()
class Apple:
    def __init__(self) -> None:
        self.pos = pygame.Vector2()
        self.vel = pygame.Vector2()
    def update(self):
        self.vel += gravity_acc
        if (self.vel > TERMINAL_VEL):
            self.vel = TERMINAL_VEL
        

    
pygame.mixer.init()
mixer.music.load("music.wav")

#player

imp_def = pygame.image.load("mam.png").convert()
imp_def = pygame.transform.scale(imp_def, (125, 125))
imp_def.set_colorkey(pygame.Color(255, 255, 255, 255))


imp_rot = pygame.transform.flip(imp_def, True, False)

imp = imp_def

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2 * 1.6)

mixer.music.play(loops=-1)

#tree
tree = pygame.image.load("tree.png").convert()
tree = pygame.transform.scale(tree, (900, 900))
tree_pos = tree.get_rect()
tree_pos.centerx = (screen.get_width() / 2)
tree_pos.centery = (screen.get_height() / 2 * 0.971)
tree.set_colorkey(pygame.Color(0, 0, 0, 255))

#sky
sky = pygame.image.load("sky.png").convert()
sky = pygame.transform.scale(sky, (1280, 800))
sky_pos = sky.get_rect()
sky_pos.centerx = (screen.get_width() / 2)
sky_pos.centery = (screen.get_height() / 2 * 0.8)


#grass
grass = pygame.image.load("grass.png").convert()
grass = pygame.transform.scale(grass, (500, 400))
grass_pos = grass.get_rect()
grass_pos.centerx = (screen.get_width() / 2)
grass_pos.centery = (screen.get_height() / 2 * 0.8)
grass.set_colorkey(pygame.Color(0, 0, 0, 255))

player_dir = pygame.Vector2()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # key handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_dir.x -= 1.0
                imp = imp_def
            if event.key == pygame.K_d:
                player_dir.x += 1.0
                imp = imp_rot
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_dir.x += 1.0
            if event.key == pygame.K_d:
                player_dir.x -= 1.0

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(sky, sky_pos)
    screen.blit(sky, sky_pos)
    screen.blit(tree, tree_pos)
    screen.blit(grass, (screen.get_width() / 2 * 1.45, screen.get_height() / 2 * 1.3))
    screen.blit(grass, (screen.get_width() / 2 * 1, screen.get_height() / 2 * 1.3))
    screen.blit(grass, (screen.get_width() / 2 * 0.5, screen.get_height() / 2 * 1.3))
    screen.blit(grass, (screen.get_width() / 2 * 0.25, screen.get_height() / 2 * 1.3))
    screen.blit(grass, (screen.get_width() / 2 * 0, screen.get_height() / 2 * 1.3))
    screen.blit(grass, (screen.get_width() / 2 -1000, screen.get_height() / 2 * 1.3))
    screen.blit(imp, (player_pos))
    
    # Player pos change
    player_pos += player_dir * 5
    
    if player_pos.x < 0 - 25:
        player_pos.x = 0 - 25
    elif player_pos.x > window_width - 100:
        player_pos.x = window_width - 100

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time ian seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
