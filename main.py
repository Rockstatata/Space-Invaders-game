import pygame as pg
import random as rd
import math as m
from pygame import mixer

# initializing the pygame
pg.init()

# create the screen
screen = pg.display.set_mode((800, 600))

# creating a background image
bg = pg.image.load("background.png")

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# running the game
running = True

# Title and icon
pg.display.set_caption("Space Invaders")
icon = pg.image.load("ufo.png")
pg.display.set_icon(icon)

# game mechanics
thresh = 10
num = 3
score = 0
collision = False
font = pg.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

# player
playerimg = pg.image.load("arcade-game.png")
playerX = 368
playerY = 468
playerX_change = 0
newplayerspeed = 5

# enemy
numofenemies = 1
newspeedX = 4
newspeedY = 20
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range(numofenemies):
    enemyimg.append(pg.image.load("pngwing.com.png"))
    enemyX.append(rd.randint(0, 720))
    enemyY.append(rd.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(20)

# bullets
bulletimg = pg.image.load("bullet.png")
bulletX = 0
bulletY = 468
bulletY_change = 10
bullet_state = "ready"  # ready = bullet can't be seen, fire = bullet is moving


# player appearing function
def player(x, y):
    screen.blit(playerimg, (x, y))


# enemy appearing function
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


# bullet firing function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))  # to center the bullet coming from spaceship


# collision function
def iscollision(enemyX, enemyY, bulletX, bulletY, i):
    distance = m.sqrt(m.pow((enemyX[i] + 30 - bulletX), 2) + m.pow((enemyY[i] + 30 - bulletY), 2))
    if distance <= 30:
        return True
    return False


# score function
def show_score(x, y):
    scorevalue = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scorevalue, (x, y))


# game over function
over_font = pg.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    mixer.music.stop()


# game loop
while running:
    # RGB screen fill
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(bg, (0, 0))

    # game quitting functionality
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # adding values to x coordinate and subtracting values from y coordinate can move the spaceship
        # if keystroke is pressed check whether its right or left
        if event.type == pg.KEYDOWN:  # a key has been pressed
            if event.key == pg.K_LEFT:
                playerX_change = -newplayerspeed
            if event.key == pg.K_RIGHT:
                playerX_change = newplayerspeed
            if event.key == pg.K_SPACE:
                if bullet_state is "ready":
                    # get the current x coordinate of the spaceship
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pg.KEYUP:  # a key has been released
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0

    # drawing player onto the screen
    playerX += playerX_change

    # Player movement
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    player(playerX, playerY)

    # increasing speed
    if score > thresh:
        thresh += 10
        newplayerspeed += 2
        newspeedX += 1
        newspeedY += 5
        for i in range(numofenemies):
            enemyX_change[i] = newspeedX
            enemyY_change[i] = newspeedY

    # increasing enemies
    if score > num:
        num += 3
        numofenemies += 1
        for i in range(numofenemies):
            enemyimg.append(pg.image.load("pngwing.com.png"))
            enemyX.append(rd.randint(0, 720))
            enemyY.append(rd.randint(50, 150))
            enemyX_change.append(newspeedX)
            enemyY_change.append(newspeedY)

    # Enemy Movement
    for i in range(numofenemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= -50 or enemyX[i] >= 720:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]

        # Game over
        if enemyY[i] >= 420:
            for j in range(numofenemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemy(enemyX[i], enemyY[i], i)
        # collision checking
        collision = iscollision(enemyX, enemyY, bulletX, bulletY, i)
        if collision is True:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = rd.randint(0, 720)
            enemyY[i] = rd.randint(50, 150)

    # Bullet movement
    if bullet_state is "fire":  # to have continuous movement of the bullet
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:  # if it goes above the screen then it resets the bullet
        bulletY = 480
        bullet_state = "ready"

    # shows the score
    show_score(scoreX, scoreY)

    pg.display.update()
