import pygame
import random as rd
import math
import sys
from pygame.locals import *
from time import sleep

delay = 1

# 초기화
pygame.init() 

# 화면 설정
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("fight game")

screen_center = [WIDTH/2, HEIGHT/2]

# 색깔 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 중력 정의

y_gravity = 1
jump_height = 20
y_velocity = jump_height
jumping = False
x_speed = 5
x_velocity = 1

# 플레이어 정의
player_x = screen_center[0]/2
player_y = screen_center[1]/2 + screen_center[1]/4
player_width = 200
player_height = 200
# (player_width, player_height)

# 변수 정의
move = False
attack01 = False
walkCount = 0
idle = True
sliding = False
dirtwidth = WIDTH
dirtheight = HEIGHT/4
player_hp = 20
key_states = {pygame.K_LEFT: False, pygame.K_RIGHT: False}
raindrops = []
last_raindrop_time = pygame.time.get_ticks()

def imgDefine(path, x, y):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (x,y))
    return img

# 이미지 정의
move1 = imgDefine("image/move_1.png", player_width, player_height)
move2 = imgDefine("image/move_2.png", player_width, player_height)
movement = [move1, move1, move1, move1, move1, move2, move2, move2, move2, move2]
idleimg = imgDefine("image/idle.png", player_width, player_height)
jumpimg = imgDefine("image/jump.png", player_width, player_height)
slideimg = imgDefine("image/slide.png", player_width, player_height)
sky = imgDefine("image/haneul.png",WIDTH,HEIGHT)
dirt = imgDefine("image/ddang.png",dirtwidth,dirtheight)
startimg = pygame.image.load("image/gamestart_01.png")
clickstartimg = pygame.image.load("image/gamestart_02.png")
# quitimg = pygame.image.load("image/gamequit_01.png")
# clickquitimg = pygame.image.load("image/gamequit_02.png")



class Raindrop:
    def __init__(self):
        self.x = rd.randint(0,WIDTH)
        self.y = -5
        self.speed = rd.randint(5,18)

    def move(self):
        self.y += self.speed
    
    def draw(self):
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (self.x, self.y+30), 30)

    def off_screen(self):
        return self.y > 800
    


class Button:
    def __init__(self, img_in, x, y, width, height, img_act, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            screen.blit(img_act,(x, y))
            if click[0] and action != None:
                sleep(1)
                action()
        else:
            screen.blit(img_in,(x,y))
        

def playerMovement():
    global walkCount, player_x, player_y

    # screen.fill(WHITE)

    if walkCount > 9:
        walkCount = 0
    if jumping == False:
        if sliding == False:
            if move == True:
                screen.blit(movement[walkCount], (player_x-player_width/2, player_y+player_height/2))
                walkCount += 1
            else:
                screen.blit(idleimg, (player_x-player_width/2, player_y+player_height/2))
        else:
            screen.blit(slideimg, (player_x-player_width/2, player_y+player_height/2))
    elif jumping == True:
        screen.blit(jumpimg, (player_x-player_width/2, player_y+player_height/2))
    else:
        screen.blit(idleimg, (player_x-player_width/2, player_y+player_height/2))

def quitGame():
    pygame.quit()
    sys.exit()

clock = pygame.time.Clock()

def mainmenu():
    menu = True
    while menu:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.blit(pygame.image.load("image/menu.png"), (0,0))
        startButton = Button(startimg,screen_center[0]-150,screen_center[1]-100,300,200,clickstartimg,mainGame)
        # quitButton = Button(quitimg,screen_center[0]-300,screen_center[1]-200,300,200,clickquitimg,quitGame)

        pygame.display.flip()

def mainGame():
    global sliding, y_velocity, jumping, move, idle, player_x, player_y, last_raindrop_time
    running = True
    while running:
        clock.tick(60)
        screen.blit(sky,(0,0))
        screen.blit(dirt,(0,HEIGHT-dirtheight))

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quitGame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    move = any(key_states.values())  # 딕셔너리 값 중 하나라도 True이면 move는 True
                    idle = not move
                    key_states[event.key] = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    key_states[event.key] = True
                    move = any(key_states.values())  # 딕셔너리 값 중 하나라도 True이면 move는 True
                    idle = not move
    
        move = any(key_states.values())  # 딕셔너리 값 중 하나라도 True이면 move는 True
        idle = not move
        
        pressed_keys = pygame.key.get_pressed()

        if not sliding:
            if pressed_keys[K_LEFT]:
                player_x -= x_speed
            if pressed_keys[K_RIGHT]:
                player_x += x_speed
            if pressed_keys[K_UP]:
                jumping = True
            # if pressed_keys[K_a]:
                # attack01 = True

        if pressed_keys[K_DOWN]:
            sliding = True
        else:
            sliding = False

    
        playerMovement()

    
        if jumping:
            player_y -= y_velocity
            y_velocity -= y_gravity
            if y_velocity < -jump_height:
                jumping = False
                y_velocity = jump_height


        # 일정 시간마다 비 생성
        
        current_timef = pygame.time.get_ticks()
        if current_timef - last_raindrop_time > 300:  # 5초에 한 번
            raindrops.append(Raindrop())
            last_raindrop_time = current_timef

        i = 0
        while i < len(raindrops) :    
            raindrops[i].move()
            raindrops[i].draw()
            if raindrops[i].off_screen():
                del raindrops[i]
                i -= 1
            i += 1   
        pygame.display.flip()
    
mainmenu()
# mainGame()