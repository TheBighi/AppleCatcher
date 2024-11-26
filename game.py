import pygame
from pygame import mixer
from pygame import KEYDOWN
import settings
from apples import Apple
import random

# pygame setup
pygame.init()
window_width = settings.window_width
window_height = settings.window_height

screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.Font(None, 36)

score = 0

#sound
pygame.mixer.init()
mixer.music.load("music.wav")
ding = pygame.mixer.Sound('ding.mp3')

# player
imp_def = pygame.image.load("mam.png").convert()
imp_def = pygame.transform.scale(imp_def, (125, 125))
imp_def.set_colorkey(pygame.Color(255, 255, 255, 255))

imp_rot = pygame.transform.flip(imp_def, True, False)

imp = imp_def

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2 * 1.6)

# tree
tree = pygame.image.load("tree.png").convert()
tree = pygame.transform.scale(tree, (900, 900))
tree_pos = tree.get_rect()
tree_pos.centerx = (screen.get_width() / 2)
tree_pos.centery = (screen.get_height() / 2 * 0.971)
tree.set_colorkey(pygame.Color(0, 0, 0, 255))

# sky
sky = pygame.image.load("sky.png").convert()
sky = pygame.transform.scale(sky, (1280, 800))
sky_pos = sky.get_rect()
sky_pos.centerx = (screen.get_width() / 2)
sky_pos.centery = (screen.get_height() / 2 * 0.8)

# grass
grass = pygame.image.load("grass.png").convert()
grass = pygame.transform.scale(grass, (500, 400))
grass_pos = grass.get_rect()
grass_pos.centerx = (screen.get_width() / 2)
grass_pos.centery = (screen.get_height() / 2 * 0.8)
grass.set_colorkey(pygame.Color(0, 0, 0, 255))

player_dir = pygame.Vector2()

# Initialize apples list as empty
apples = []

# Apple spawn frequency and count
apple_spawn_timer = 0
max_apples_to_spawn = 2  # Max number of apples to spawn at once (random between 1 and max_apples_to_spawn)
spawn_interval = 30  # Interval in frames to check for apple spawning

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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

    # Update player position
    player_pos += player_dir * 1
    if player_pos.x < -25:
        player_pos.x = -25
    elif player_pos.x > window_width - imp.get_width():
        player_pos.x = window_width - imp.get_width()

    # Define player rectangle based on the current player position
    player_rect = pygame.Rect(player_pos.x, player_pos.y, imp.get_width(), imp.get_height())

    # Update apples and check for collisions
    for apple in apples[:]:
        apple.update()
        if apple.check_collision(player_rect):
            score += 1
            apples.remove(apple)  # Remove apple on collision
            ding.play()

        if apple.rect.y > window_height:  # Remove apple if it falls off the screen
            apples.remove(apple)

    # Spawn new apples every few frames
    apple_spawn_timer += 1
    if apple_spawn_timer >= spawn_interval:
        apple_spawn_timer = 0
        apples_to_spawn = random.randint(1, 1)
        for _ in range(apples_to_spawn):
            apples.append(Apple(window_width, window_height))

    # Fill the screen with a color to wipe away anything from the last frame
    screen.blit(sky, sky_pos)
    screen.blit(sky, sky_pos)
    screen.blit(tree, tree_pos)
    screen.blit(grass, (screen.get_width() / 2 * 1.45, screen.get_height() / 2 * 1.3))
    screen.blit(grass, (screen.get_width() / 2 * 1, screen.get_height() / 2 * 1.3))
    screen.blit(grass, (screen.get_width() / 2 * 0.5, screen.get_height() / 2 * 1.3))
    screen.blit(grass, (screen.get_width() / 2 * -0.55, screen.get_height() / 2 * 1.3))
    screen.blit(imp, (player_pos))

    # Draw apples
    for apple in apples:
        apple.draw(screen)

    # Player pos change
    player_pos += player_dir * settings.player_speed
    if player_pos.x < 0 - 25:
        player_pos.x = 0 - 25
    elif player_pos.x > window_width - 100:
        player_pos.x = window_width - 100

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Draw player rectangle for debugging
    pygame.draw.rect(screen, (0, 255, 0), player_rect, 2)  # Green rectangle for player

    # Draw apple rectangles for debugging
    for apple in apples:
        pygame.draw.rect(screen, (255, 0, 0), apple.rect, 2)  # Red rectangles for apples

    # Update the display
    pygame.display.flip()

    # Limit FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
