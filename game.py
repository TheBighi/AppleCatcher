import time
import pygame
from pygame import mixer
from pygame import KEYDOWN
import settings
from apples import Apple
import random

# pygame setup
pygame.init()

screen = pygame.display.set_mode((settings.window_width, settings.window_height))
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.Font(None, 36)

score = 0

#sound
pygame.mixer.init()
music = pygame.mixer.Sound("music.mp3")
ding = pygame.mixer.Sound('ding.mp3')
music.set_volume(0.075)
music.play(loops=-1) # REMIND CAHNGE DING SOUND EFFECT LOUDER!!!!!!!!!!!

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

player_speed = settings.player_speed

# Apple spawn frequency and count
apple_spawn_timer = 0
spawn_interval = 60  # Interval in frames to check for apple spawning
min_apples_to_spawn = 1
max_apples_to_spawn = 2


power_up1 = False
power_up1_time = 0

debuff1 = False
debuff1_current_time = 0
debuff1_time = 4000 # ms 
counterdebuff = 0

apples_lost = 0

def apple_uh():
    global apples_lost
    apples_lost += 1

while running:
    # power up
    if score > 10 and not power_up1 and score < 31:
        power_up1 = True
        power_up1_time = pygame.time.get_ticks()
    if power_up1:
        player_speed = 15
        if pygame.time.get_ticks() - power_up1_time > 10000:
            power_up1 = False
            player_speed = settings.player_speed
    if apples_lost >= 10 and not debuff1 and counterdebuff == 0:
        debuff1 = True
        debuff1_current_time = pygame.time.get_ticks()
    if debuff1:
        
        settings.GRAV = 6
        for apple in apples:
            apple.speed = settings.GRAV
        if pygame.time.get_ticks() - debuff1_current_time > debuff1_time:
            counterdebuff += 1
            debuff1 = False
            settings.GRAV = 3
            print("misiganes")

    # made for direction changes
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
#    if apples_lost >= settings.fail_condition:
#       running = False

    # player pos update
    player_pos += player_dir * 1
    if player_pos.x < -25:
        player_pos.x = -25
    elif player_pos.x > settings.window_width - imp.get_width():
        player_pos.x = settings.window_width - imp.get_width()

    # Define player rectangle based on the current player position
    player_rect = pygame.Rect(player_pos.x, player_pos.y, imp.get_width(), imp.get_height())

    # apple collision checlk
    for apple in apples[:]:
        apple.update()
        if apple.check_collision(player_rect):
            score += 1
            apples.remove(apple)  # Remove apple on collision
            ding.play()
            

    # Spawn new apples every few frames
    apple_spawn_timer += 1
    if apple_spawn_timer >= spawn_interval:
        apple_spawn_timer = 0
        apples_to_spawn = random.randint(min_apples_to_spawn, max_apples_to_spawn)
        for _ in range(apples_to_spawn):
            apples.append(Apple(settings.window_width, settings.window_height, update_hook=apple_uh))
            

    # 
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
    player_pos += player_dir * player_speed
    if player_pos.x < 0 - 25:
        player_pos.x = 0 - 25
    elif player_pos.x > settings.window_width - 100:
        player_pos.x = settings.window_width - 100

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Display apples lost
    applesl_text = font.render(f"Apples lost: {apples_lost}", True, (255, 255, 255))
    screen.blit(applesl_text, (10, 45))

    #if debuff1 and :
    #    debufftimer = font.render(f"Debuff will be active for 5 seconds", True, (255, 255, 255))
    #    screen.blit(debufftimer, (10, 70))

    # Draw player rectangle for debugging
    #pygame.draw.rect(screen, (0, 255, 0), player_rect, 2)  # Green rectangle for player

    # Draw apple rectangles for debugging
    #for apple in apples:
    #    pygame.draw.rect(screen, (255, 0, 0), apple.rect, 2)  # Red rectangles for apples

    # Update the display
    pygame.display.flip()

    # Limit FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
