# Example file showing a circle moving on screen
import pygame
from pygame import mixer
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
apple_img = pygame.image.load("C:\\Users\\sander.tamm\\Downloads\\apple.png").convert()
dt = 0

gravity_acc = pygame.Vector2(0.0, 1.2)
TERMINAL_VEL = 10

class Apple:
    def __init__(self) -> None:
        self.pos = pygame.Vector2()
        self.vel = pygame.Vector2()
    def update(self):
        self.vel += gravity_acc
        if (self.vel > TERMINAL_VEL):
            self.vel = TERMINAL_VEL
        

    
pygame.mixer.init()
mixer.music.load("C:\\Users\\sander.tamm\\Downloads\\music.wav")

#player
imp = pygame.image.load("C:\\Users\\sander.tamm\\Downloads\\mam.png").convert()
imp = pygame.transform.scale(imp, (125, 125))
imp.set_colorkey(pygame.Color(255, 255, 255, 255))
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2 * 1.6)

mixer.music.play(loops=-1)

#tree
tree = pygame.image.load("C:\\Users\\sander.tamm\\Downloads\\tree.png").convert()
tree = pygame.transform.scale(tree, (900, 900))
tree_pos = tree.get_rect()
tree_pos.centerx = (screen.get_width() / 2)
tree_pos.centery = (screen.get_height() / 2 * 0.971)
tree.set_colorkey(pygame.Color(0, 0, 0, 255))

#sky
sky = pygame.image.load("C:\\Users\\sander.tamm\\Downloads\\sky.png").convert()
sky = pygame.transform.scale(sky, (1280, 800))
sky_pos = sky.get_rect()
sky_pos.centerx = (screen.get_width() / 2)
sky_pos.centery = (screen.get_height() / 2 * 0.8)


#grass
grass = pygame.image.load("C:\\Users\\sander.tamm\\Downloads\\grass.png").convert()
grass = pygame.transform.scale(grass, (500, 400))
grass_pos = grass.get_rect()
grass_pos.centerx = (screen.get_width() / 2)
grass_pos.centery = (screen.get_height() / 2 * 0.8)
grass.set_colorkey(pygame.Color(0, 0, 0, 255))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    
    
    

    keys = pygame.key.get_pressed()

   
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time ian seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
