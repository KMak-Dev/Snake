# Music: https://www.bensound.com


import random
import pygame
import time
from pygame import mixer
from pygame import mixer_music
pygame.init()
pygame.mixer.pre_init(44100,16,1,512)

# Global Variables
gameOver = False
running = True
HEIGHT = 600
WIDTH = 600
GRID_SIZE = 30
playerX = WIDTH / 2
playerY = HEIGHT / 2
fruitX = random.randint(0, 15) * GRID_SIZE
fruitY = random.randint(0, 15) * GRID_SIZE
random.seed(time.process_time())
dir = 5
score = 0
numTail = 0
tailX = []
tailY = []

# Screen-Title And Icon
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("Python !")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
font = pygame.font.Font('freesansbold.ttf', 20)
font2 = pygame.font.Font('freesansbold.ttf',1000000)

# Textures
background = pygame.image.load('Background.png')
snake = pygame.image.load('snake.png')
fruit = pygame.image.load('fruit.png')
Snake = []
gameOvr = font.render(" GAME OVER! ", True, (255, 255, 255))

# Music / Sound
pygame.mixer.music.load('funky.wav')
pygame.mixer.music.play(-1)
death_sound = pygame.mixer.Sound('hit.wav')
score_sound = pygame.mixer.Sound('score.wav')

# Functions
def fruitGen():
    global fruitX
    global fruitY
    fruitX = random.randint(0, 15) * GRID_SIZE
    fruitY = random.randint(2, 15) * GRID_SIZE


def draw():
    global score
    global numTail
    time.sleep(0.15)
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(fruit, (fruitX, fruitY))
    screen.blit(snake, (playerX, playerY))
    scor = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scor, (0, HEIGHT / 2 - 300))
    index = 0
    while index < numTail:
        screen.blit(Snake[index], (tailX[index], tailY[index]))
        index += 1


def moveHead(direction):
    global playerX
    global playerY
    if direction == 0:
        playerY -= GRID_SIZE
        return
    if direction == 1:
        playerY += GRID_SIZE
        return
    if direction == 2:
        playerX -= GRID_SIZE
        return
    if direction == 3:
        playerX += GRID_SIZE
        return


def checkGameOver(x, y):
    global WIDTH
    global HEIGHT
    if x > WIDTH or y > HEIGHT or x < 0 or y < 0:
        return True
    i = 0
    while i < numTail:
        if playerX == tailX[i] and playerY == tailY[i]:
            return True
        i += 1
    return False


def checkFruitEaten(pX, pY, fX, fY):
    global score
    if pX == fX and pY == fY:
        fruitGen()
        score += 1
        return True


def logic():
    global gameOver
    global numTail
    global tailX
    global tailY
    gameOver = checkGameOver(playerX, playerY)
    if checkFruitEaten(playerX, playerY, fruitX, fruitY):
        score_sound.play()
        numTail += 1
        tailX.append(0)
        tailY.append(0)
        Snake.append(pygame.image.load('snake.png'))

    prevX = playerX
    prevY = playerY
    moveHead(dir)
    i = 0
    while i < numTail:
        prev2X = tailX[i]
        prev2Y = tailY[i]
        tailX[i] = prevX
        tailY[i] = prevY
        prevX = prev2X
        prevY = prev2Y
        i += 1

i = 0
# Main Game-loop
while running:
    if gameOver != True:
        logic()
        draw()
    else:
        screen.blit(gameOvr,(235,HEIGHT/2-30))
        pygame.mixer.music.stop()
        if i == 0:
            death_sound.play()
            i += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                dir = 2
            if event.key == pygame.K_w:
                dir = 0
            if event.key == pygame.K_d:
                dir = 3
            if event.key == pygame.K_s:
                dir = 1
    pygame.display.update()
