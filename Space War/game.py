# 1 - Import library
import pygame
from pygame.locals import *
import math
import random

# 2 - Initialize the game
pygame.init()
width, height = 640, 480
screen=pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos=[100,100]
acc=[0,0]
bullets=[]
badtimer=100
badtimer1=0
aliens=[[640, 100]]
healthvalue=194
accuracy = 0
running = 1
exitcode = 1
pygame.mixer.init()
start_time = 0
roundtime = 60000

# 3 - Load image
player = pygame.image.load("resources/images/aircraft.png")
backgroundImage = pygame.image.load("resources/images/newBackground.jpg")
earth = pygame.image.load("resources/images/earth.png")
arrow = pygame.image.load("resources/images/bullet.png")
alienimg1 = pygame.image.load("resources/images/alien.png")
alienimg=alienimg1
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/winner.png")
# 3.1 - Load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/backgroundNoise.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


def game_intro():
    global start_time
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        introText = pygame.font.SysFont("comicsansms", 72).render("Space War", True, (255, 255, 255))
        gameInfo = pygame.font.SysFont("comicsansms", 24).render("Use 'W' or 'S' + MOUSE to move and LBUTTON for shooting", True, (255, 255, 255))
        screen.fill((3, 30, 1))
        screen.blit(introText, (220, 40))
        screen.blit(backgroundImage, (640, 480))
        button("GO!", 270, 350, 110, 60, (43, 66, 24), (80, 122, 45), game)
        screen.blit(gameInfo, (220, 570))
        pygame.display.update()


def gameOver_outro():
    global accuracy
    outro = True
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: " + str(accuracy) + "%", True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(gameover, (0, 0))
    screen.blit(text, textRect)

    while outro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Play Again!", 270, 350, 110, 60, (43, 66, 24), (80, 122, 45), game_restart)
        pygame.display.update()


def gameWin_outro():
    global accuracy
    outro = True

    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: " + str(accuracy) + "%", True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(youwin, (0, 0))
    screen.blit(text, textRect)


    while outro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Play Again!", 270, 350, 110, 60, (43, 66, 24), (80, 122, 45), game_restart)
        pygame.display.update()


def game_restart():
    global playerpos, keys, start_time, acc, aliens, bullets

    aliens = [[640, 100]]
    restart = True
    bullets = []
    acc = [0, 0]
    playerpos = [100,100]
    keys = [False, False, False, False]

    while restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        start_time = pygame.time.get_ticks()
        game()
        pygame.display.update()


def game():
    # 4 - keep looping through
    global running, exitcode, accuracy
    start_time = pygame.time.get_ticks()
    running = 1
    exitcode = 0

    healthvalue = 194
    badtimer = 100
    badtimer1 = 0

    while running:
        badtimer -= 1
        # 5 - clear the screen before drawing it again
        screen.fill(0)
        # 6 - draw the player on the screen at X:100, Y:100
        for x in range(int(height / backgroundImage.get_height() + 1)):
            for y in range(int(height / backgroundImage.get_height() + 1)):
                screen.blit(backgroundImage, (x * 100, y * 100))
        screen.blit(earth, (0, 200))
        # 6.1 - Set player position and rotation
        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))
        playerrot = pygame.transform.rotate(player, 360 - angle * 57.29)
        playerpos1 = (playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)
        screen.blit(playerrot, playerpos1)
        # 6.2 - Draw bullets
        for bullet in bullets:
            index = 0
            velx = math.cos(bullet[0]) * 10
            vely = math.sin(bullet[0]) * 10
            bullet[1] += velx
            bullet[2] += vely
            if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
                bullets.pop(index)
            index += 1
            for projectile in bullets:
                arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
                screen.blit(arrow1, (projectile[1], projectile[2]))
        # 6.3 - Draw badgers
        if badtimer == 0:
            aliens.append([640, random.randint(50, 430)])
            badtimer = 100 - (badtimer1 * 2)
            if badtimer1 >= 35:
                badtimer1 = 35
            else:
                badtimer1 += 5
        index = 0
        for badguy in aliens:
            if badguy[0] < -64:
                aliens.pop(index)
            badguy[0] -= 7
            # 6.3.1 - Attack castle
            badrect = pygame.Rect(alienimg.get_rect())
            badrect.top = badguy[1]
            badrect.left = badguy[0]
            if badrect.left < 64:
                hit.play()
                healthvalue -= random.randint(5, 20)
                aliens.pop(index)
            # 6.3.2 - Check for collisions
            index1 = 0
            for bullet in bullets:
                bullrect = pygame.Rect(arrow.get_rect())
                bullrect.left = bullet[1]
                bullrect.top = bullet[2]
                if badrect.colliderect(bullrect):
                    enemy.play()
                    acc[0] += 1
                    aliens.pop(index)
                    bullets.pop(index1)
                index1 += 1
            # 6.3.3 - Next bad guy
            index += 1
        for badguy in aliens:
            screen.blit(alienimg, badguy)
        # 6.4 - Draw clock
        font = pygame.font.Font(None, 24)
        time_since_enter = pygame.time.get_ticks() - start_time
        survivedtext = font.render(str((roundtime - time_since_enter) / 1000 % 60).zfill(2), True, (0, 0, 0))
        textRect = survivedtext.get_rect()
        textRect.topright = [635, 5]
        screen.blit(survivedtext, textRect)
        # 6.5 - Draw health bar
        screen.blit(healthbar, (5, 5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1 + 8, 8))
        # 7 - update the screen
        pygame.display.flip()
        # 8 - loop through the events
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type == pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    keys[0] = True
                elif event.key == K_a:
                    keys[1] = True
                elif event.key == K_s:
                    keys[2] = True
                elif event.key == K_d:
                    keys[3] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    keys[0] = False
                elif event.key == pygame.K_a:
                    keys[1] = False
                elif event.key == pygame.K_s:
                    keys[2] = False
                elif event.key == pygame.K_d:
                    keys[3] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                shoot.play()
                position = pygame.mouse.get_pos()
                acc[1] += 1
                bullets.append([math.atan2(position[1] - (playerpos1[1] + 32), position[0] - (playerpos1[0] + 26)),
                                playerpos1[0] + 32, playerpos1[1] + 32])

        # 9 - Move player
        if keys[0]:
            playerpos[1] -= 5
        elif keys[2]:
            playerpos[1] += 5
        if keys[1]:
            playerpos[0] -= 5
        elif keys[3]:
            playerpos[0] += 5

        # 10 - Win/Lose check
        time_since_enter = pygame.time.get_ticks() - start_time
        if time_since_enter >= roundtime:
            running = 0
            exitcode = 1
        if healthvalue <= 0:
            running = 0
            exitcode = 0
        if acc[1] != 0:
            accuracy = acc[0] * 1.0 / acc[1] * 100
        else:
            accuracy = 0
    # 11 - Win/lose display
    if exitcode == 0:
        gameOver_outro()
    else:
        gameWin_outro()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()

game_intro()
game()

