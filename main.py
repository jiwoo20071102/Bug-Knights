import pygame
import random as rd
import sys
from pygame.locals import *
from time import sleep

delay = 1

# 초기화
pygame.init() 

# 화면 설정
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BUG KNIGHTS")

screen_center = [WIDTH/2, HEIGHT/2]

# 색깔 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 변수 정의
dirtwidth = WIDTH
dirtheight = HEIGHT/4
raindrops = []
last_raindrop_time = pygame.time.get_ticks()
score = 0

def imgDefine(path, x, y):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (x,y))
    return img

# 이미지 정의
sky = imgDefine("image/haneul.png",WIDTH,HEIGHT)
dirt = imgDefine("image/ddang.png",dirtwidth,dirtheight)
startimg = pygame.image.load("image/gamestart_01.png")
clickstartimg = pygame.image.load("image/gamestart_02.png")
waterimg = imgDefine("image/water.png", 100, 100)
quitimg = pygame.image.load("image/gamequit_01.png")
clickquitimg = pygame.image.load("image/gamequit_02.png")
menuimg = imgDefine("image/menu.png", WIDTH,HEIGHT)

move1 = imgDefine("image/player_0.png", 128, 128)
move2 = imgDefine("image/player_1.png", 128, 128)
move3 = imgDefine("image/player_2.png", 128, 128)
move4 = imgDefine("image/player_3.png", 128, 128)

# 기타 정의
font = pygame.font.SysFont(None, 50)


class Raindrop:
    def __init__(self):
        self.x = rd.randint(100,WIDTH-100)
        self.y = -100
        self.speed = rd.randint(5,15)

    def move(self):
        self.y += self.speed
    
    def draw(self):
        screen.blit(waterimg, (self.x, self.y))

    def off_screen(self):
        return self.y > 900


class Player:
    def __init__(self):
        self.x = screen_center[0]
        self.y = screen_center[1]
        self.speed = 5
        self.heading = 1

    def left(self):
        self.x -= self.speed
        self.heading = 4
    
    def right(self):
        self.x += self.speed
        self.heading = 2

    def up(self):
        self.y -= self.speed
        self.heading = 3
    
    def down(self):
        self.y += self.speed
        self.heading = 1
    
    def draw(self):
        if self.heading == 1:
            screen.blit(move1,(self.x,self.y))
        if self.heading == 2:
            screen.blit(move2,(self.x,self.y))
        if self.heading == 3:
            screen.blit(move3,(self.x,self.y))
        if self.heading == 4:
            screen.blit(move4,(self.x,self.y))

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

def quitGame():
    pygame.quit()
    sys.exit()

clock = pygame.time.Clock()

def mainmenu():
    menu = True
    while menu:
        clock.tick(75)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.blit(menuimg, (0,0))
        startButton = Button(startimg,screen_center[0]-150,screen_center[1]-110,300,200,clickstartimg,mainGame)
        quitButton = Button(quitimg,screen_center[0]-150,screen_center[1]+100,300,200,clickquitimg,quitGame)

        pygame.display.flip()

def mainGame():
    global move, last_raindrop_time, score
    players = Player()
    running = True
    while running:
        clock.tick(75)
        screen.blit(sky,(0,0))
        screen.blit(dirt,(0,HEIGHT-dirtheight))

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quitGame()
        
        pressed_keys = pygame.key.get_pressed()

        players.draw()

        if pressed_keys[K_LEFT]:
            players.left()
        if pressed_keys[K_RIGHT]:
            players.right()
        if pressed_keys[K_UP]:
            players.up()
        if pressed_keys[K_DOWN]:
            players.down()

        # 일정 시간마다 비 생성
        
        current_timef = pygame.time.get_ticks()
        if current_timef - last_raindrop_time > 3000:  # 3초에 한번
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