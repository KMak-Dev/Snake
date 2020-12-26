# Music: https://www.bensound.com


import random
import time
import pygame

pygame.init()
pygame.mixer.pre_init(44100, 16, 1, 512)


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
direction = 5
score = 0
numTail = 0
tailX = []
tailY = []
Menu = True


# Screen-Title And Icon
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("Python !")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
font = pygame.font.Font('freesansbold.ttf', 20)
font2 = pygame.font.Font('freesansbold.ttf', 50)
font3 = pygame.font.Font('freesansbold.ttf', 50)
flashing = 0


# Textures
background = pygame.image.load('Background.png')
snake = pygame.image.load('snake.png')
fruit = pygame.image.load('fruit.png')
Snake = []
instruction = font.render("Press Space To Start", True, (254, 254, 254))
gameOvr = font2.render(" GAME OVER! ", True, (254, 254, 254))
title = font3.render("PYTHON !", True, (254, 254, 254))


# Music / Sound
pygame.mixer.music.load('funky.wav')
death_sound = pygame.mixer.Sound('hit.wav')
score_sound = pygame.mixer.Sound('score.wav')


# Functions
def generate_fruit():
    global fruitX
    global fruitY
    fruitX = random.randint(0, 15) * GRID_SIZE
    fruitY = random.randint(2, 15) * GRID_SIZE


def draw():
    global score
    global numTail
    time.sleep(0.10)
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(fruit, (fruitX, fruitY))
    screen.blit(snake, (playerX, playerY))
    index = 0
    score_display = font.render("Score: " + str(score), True, (254, 254, 254))
    while index < numTail:
        screen.blit(Snake[index], (tailX[index], tailY[index]))
        index += 1
    screen.blit(score_display, (0, HEIGHT / 2 - 300))


def move_Head(direction):
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


def check_Game_Over(x, y):
    global WIDTH
    global HEIGHT
    if x > WIDTH or y > HEIGHT or x < 0 or y < 0:
        return True
    index = 0
    while index < numTail:
        if playerX == tailX[index] and playerY == tailY[index]:
            return True
        index += 1
    return False


def check_Fruit_Eaten(player_x, player_y, fruit_x, fruit_y):
    global score
    if player_x == fruit_x and player_y == fruit_y:
        generate_fruit()
        score += 1
        return True


def logic():
    global gameOver
    global numTail
    global playerX
    global playerY
    global tailX
    global tailY
    gameOver = check_Game_Over(playerX, playerY)
    if check_Fruit_Eaten(playerX, playerY, fruitX, fruitY):
        score_sound.play()
        numTail += 1
        tailX.append(0)
        tailY.append(0)
        Snake.append(pygame.image.load('snake.png'))
    prevX = playerX
    prevY = playerY
    move_Head(direction)
    index = 0
    while index < numTail:
        prev2X = tailX[index]
        prev2Y = tailY[index]
        tailX[index] = prevX
        tailY[index] = prevY
        prevX = prev2X
        prevY = prev2Y
        index += 1


def end(count):
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    score_display = font.render("Score: " + str(score), True, (254, 254, 254))
    screen.blit(gameOvr, (WIDTH / 2 - 170, HEIGHT / 2 - 50))
    screen.blit(score_display, (0, HEIGHT / 2 - 300))
    if count == 0:
        death_sound.play()
        count += 1
    return count


# Handling Music
from_menu = False
death_sound_count = 0
music_count = 0


# Main Game-loop
while running:
    if not gameOver or Menu:
        if music_count < 1:
            pygame.mixer.music.play(-1)
            music_count += 1
    if Menu:
        time.sleep(0.2)
        flashing += 1
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(title, (WIDTH / 2 - 110, HEIGHT / 2 - 200))
        if flashing % 2 == 0:
            screen.blit(instruction, (WIDTH / 2 - 80, HEIGHT / 2 + 100))
        screen.blit(snake, (WIDTH / 2, HEIGHT / 2))
    elif not gameOver and not Menu:
        draw()
        logic()
    else:
        death_sound_count = end(death_sound_count)
        if music_count < 2:
            pygame.mixer.music.stop()
            music_count += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                direction = 0
            if event.key == pygame.K_s:
                direction = 1
            if event.key == pygame.K_a:
                direction = 2
            if event.key == pygame.K_d:
                direction = 3
            if Menu and event.key == pygame.K_SPACE:
                Menu = False
            if gameOver and event.key == pygame.K_SPACE:
                Menu = False
                gameOver = False
                playerX = WIDTH / 2
                playerY = HEIGHT / 2
                direction = 5
                score = 0
                numTail = 0
                tailX = []
                tailY = []
                death_sound_count = 0
                if not from_menu:
                    music_count = 0
                from_menu = False
            if gameOver and event.key == pygame.K_ESCAPE:
                flashing = 0
                Menu = True
                music_count = 0
                from_menu = True
    pygame.display.update()
