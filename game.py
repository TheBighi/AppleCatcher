import pygame
import settings
pygame.init()
screen = pygame.display.set_mode((settings.window_width, settings.window_height))
from pygame import mixer
from pygame import KEYDOWN
from apples import Apple
import random
from menu import Button

# pygame setup

clock = pygame.time.Clock()
start_screen = True
running = True
game_running = False
fail_screen = True
dt = 0
font = pygame.font.Font("font.TTF", 36)
font2 = pygame.font.Font("font.TTF", 18)

high_score = 0

#võtab highscori txt failist
with open ("highscore.txt", "r") as f:
    hsl = f.readline()
    high_score = int(hsl.strip())
high_score_display = high_score

score = 0

# sounds
pygame.mixer.init()
music = pygame.mixer.Sound("music.mp3")
ding = pygame.mixer.Sound('ding.mp3')
badsfx = pygame.mixer.Sound("badsfx.mp3")
music.set_volume(0.075)
music.play(loops=-1) # REMIND CAHNGE DING SOUND EFFECT LOUDER!!!!!!!!!!!


# player
imp_def = pygame.image.load("mam.png").convert()
imp_def = pygame.transform.scale(imp_def, (125, 125))
imp_def.set_colorkey(pygame.Color(255, 255, 255, 255))
imp_rot = pygame.transform.flip(imp_def, True, False)
imp = imp_def
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2 * 1.6)
player_speed = settings.player_speed

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

# movement
player_dir = pygame.Vector2()

# Initialize õuna list tühjana
apples = []


# õuna spawn sagedus 
apple_spawn_timer = 0
spawn_interval = settings.spawn_apple_interval  # Interval in frames to check for apple spawning
min_apples_to_spawn = 1
max_apples_to_spawn = 2

# power up stuff
power_up1 = False
power_up1_time = 0
power_up1_ready = False

# debuff stuff
debuff1 = False
debuff1_current_time = 0
debuff1_time = 4000 # ms 
counterdebuff = 0

apples_lost = 0

# functions to work with menu.py
def start():
    global game_running
    game_running = True

def quit():
    exit(0)

def suva():
    pass

start_btn = Button(screen, start, (settings.window_width / 2, settings.window_height / 2), "Start", "font.ttf", 50)
quit_btn = Button(screen, quit, (settings.window_width / 2, settings.window_height / 2 + 125), "Quit", "font.ttf", 50)
titlebtn = Button(screen, suva, (settings.window_width / 2, settings.window_height / 2 - 200), "Apple Catching Game", "font.ttf", 50)

# update õunad kaotud scori
def apple_uh():
    global apples_lost
    apples_lost += 1

while running:
    # power up
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # movement
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
        # aktiveerib power upi kui vajutad e-d ja power up on valmis
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e and power_up1_ready:
            print("Power-up activated!")
            power_up1_ready = False
            power_up1 = True
            power_up1_time = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_running:
                start_btn.check_click()
                quit_btn.check_click()
    
    # main menu
    if not game_running:
        screen.fill((0, 0, 0))
        start_btn.update()
        quit_btn.update()
        titlebtn.draw()

        pygame.display.flip()
        # Limit FPS to 60
        dt = clock.tick(60) / 1000
        continue
    # power upi asi
    if score != 0 and score % 15 == 0 and not power_up1:
        power_up1_ready = True
    if power_up1:
        player_speed = 15
    if pygame.time.get_ticks() - power_up1_time > 8000:
        power_up1 = False
        player_speed = settings.player_speed
    # debuffi asi
    if apples_lost != 0 and apples_lost % 5 == 0 and not debuff1:
        debuff1 = True
        debuff1_current_time = pygame.time.get_ticks()
    if debuff1:
        settings.GRAV = 5
        spawn_interval = 30
        for apple in apples:
            apple.speed = settings.GRAV
        if pygame.time.get_ticks() - debuff1_current_time > debuff1_time:
            counterdebuff += 1
            debuff1 = False
            settings.GRAV = 3
            spawn_interval = settings.spawn_apple_interval
            print("misiganes")
    # failib kui oled liiga palju õunu kaotand
    if apples_lost >= settings.fail_count:
        running = False

    # player pos update
    player_pos += player_dir * 1
    if player_pos.x < -25:
        player_pos.x = -25
    elif player_pos.x > settings.window_width - imp.get_width():
        player_pos.x = settings.window_width - imp.get_width()

    # player rect asi
    player_rect = pygame.Rect(player_pos.x, player_pos.y, imp.get_width(), imp.get_height())

    # apple collision checlk
    for apple in apples[:]:
        apple.update()
        if apple.check_collision(player_rect):
            score += 1
            apples.remove(apple)  # kustutab  õuna kui collidib õunaga
            ding.play()
            

    # spawn õun
    apple_spawn_timer += 1
    if apple_spawn_timer >= spawn_interval:
        apple_spawn_timer = 0
        apples_to_spawn = random.randint(min_apples_to_spawn, max_apples_to_spawn)
        for _ in range(apples_to_spawn):
            apples.append(Apple(settings.window_width, settings.window_height, update_hook=apple_uh))
    # highscore näitaja variable
    if score > high_score_display:
        high_score_display = score
    # spawnib kõik backgroundi sisse ja playeri
    screen.blit(sky, sky_pos)
    screen.blit(sky, sky_pos)
    screen.blit(tree, tree_pos)
    screen.blit(grass, (screen.get_width() / 2 * 1.45, screen.get_height() / 2 * 1.3))
    screen.blit(grass, (screen.get_width() / 2 * 1, screen.get_height() / 2 * 1.3))
    screen.blit(grass, (screen.get_width() / 2 * 0.5, screen.get_height() / 2 * 1.3))
    screen.blit(grass, (screen.get_width() / 2 * -0.55, screen.get_height() / 2 * 1.3))
    screen.blit(imp, (player_pos))

    # joonistab õunu
    for apple in apples:
        apple.draw(screen)
    # player positsiooni muutja
    player_pos += player_dir * player_speed
    if player_pos.x < 0 - 25:
        player_pos.x = 0 - 25
    elif player_pos.x > settings.window_width - 100:
        player_pos.x = settings.window_width - 100

    # näitab scori
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  
    screen.blit(score_text, (10, 10))
    # näitab high scori
    high_score_text = font.render(f"High Score: {high_score_display}", True, (255, 255, 255))  
    screen.blit(high_score_text, (10, 75))

    # näitab palju õune oled kaotand
    applesl_text = font.render(f"Apples lost: {apples_lost}", True, (255, 255, 255))
    screen.blit(applesl_text, (10, 140))
    # power up ready tekst
    if power_up1_ready:
        poweruptext1 = font2.render(f"Power up ready, press e to activate.", True, (255, 255, 255))
        screen.blit(poweruptext1, (150, 675))
    # debuff text
    if debuff1:
        debuff1_text = font.render(f"Debuff active", True, (255, 255, 255))
        screen.blit(debuff1_text, (10, 205))

    # Update the display
    pygame.display.flip()

    # Limit FPS to 60
    dt = clock.tick(60) / 1000

# nuppud fail screeniks
quit_btn2 = Button(screen, quit, (settings.window_width / 2, settings.window_height / 2), "Quit", "font.ttf", 50)
failbtn2 = Button(screen, suva, (settings.window_width / 2, settings.window_height / 2 - 200), "You have failed", "font.ttf", 50)
failbtn3 = Button(screen, suva, (settings.window_width / 2, settings.window_height / 2 - 100), f"You lost {apples_lost} apples", "font.ttf", 50)

while fail_screen:
    # kui score on suurem kui high scoore savib see scori high scorina "highscore.txt" faili
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as file:
            file.write(str(high_score))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            quit_btn2.check_click()

    screen.fill((0, 0, 0))
    # nuppude joonistamine
    quit_btn2.update()
    failbtn2.draw()
    failbtn3.draw()

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
