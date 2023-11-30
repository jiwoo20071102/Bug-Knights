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
BLACK = (0,0,0)

# 변수 정의
down = []
up = []
left = []
right = []
last_raindrop_time = pygame.time.get_ticks()
score = 0

def imgDefine(path, x, y):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (x,y))
    return img

def play_sound(sound):
    channel = pygame.mixer.find_channel()  # 빈 오디오 채널 찾기
    if channel:
        channel.play(sound)

# 이미지 정의
backgroundimg = imgDefine("resource/ui/background.png",WIDTH,HEIGHT).convert()
startimg = pygame.image.load("resource/ui/gamestart_01.png")
clickstartimg = pygame.image.load("resource/ui/gamestart_02.png")
waterimg = imgDefine("resource/object/water.png", 100, 100)
quitimg = pygame.image.load("resource/ui/gamequit_01.png")
clickquitimg = pygame.image.load("resource/ui/gamequit_02.png")
menuimg = imgDefine("resource/ui/menu.png", WIDTH,HEIGHT).convert()

move1 = imgDefine("resource/playermovement/player_0.png", 100, 100)
move2 = imgDefine("resource/playermovement/player_1.png", 100, 100)
move3 = imgDefine("resource/playermovement/player_2.png", 100, 100)
move4 = imgDefine("resource/playermovement/player_3.png", 100, 100)

# 기타 정의
score_font = pygame.font.Font("resource/fonts/jua.ttf",50)
score_text_position = (10, 10)
menu_font = pygame.font.Font("resource/fonts/jua.ttf",130)

# 사운드 이펙트 정의
water_sound1 = pygame.mixer.Sound("resource/sounds/pew1.mp3")
water_sound2 = pygame.mixer.Sound("resource/sounds/pew2.mp3")
pygame.mixer.music.load("resource/sounds/background_music.mp3")


class bulletDown:
    def __init__(self):
        self.x = rd.randint(100,WIDTH-100)
        self.y = -100
        self.speed = 10
        play_sound(water_sound1)

    def move(self):
        self.y += self.speed
    
    def draw(self):
        screen.blit(waterimg, (self.x, self.y))

    def off_screen(self):
        return self.y > HEIGHT

class bulletUp:
    def __init__(self):
        self.x = rd.randint(100,WIDTH-100)
        self.y = HEIGHT+100
        self.speed = 10

    def move(self):
        self.y -= self.speed
    
    def draw(self):
        screen.blit(waterimg, (self.x, self.y))

    def off_screen(self):
        return self.y < -100

class bulletRight:
    def __init__(self):
        self.x = WIDTH + 100
        self.y = rd.randint(100,HEIGHT-100)
        self.speed = 10

    def move(self):
        self.x -= self.speed
    
    def draw(self):
        screen.blit(waterimg, (self.x, self.y))

    def off_screen(self):
        return self.x < -100

class bulletLeft:
    def __init__(self):
        self.x = -100
        self.y = rd.randint(100,HEIGHT-100)
        self.speed = 10

    def move(self):
        self.x += self.speed
    
    def draw(self):
        screen.blit(waterimg, (self.x, self.y))

    def off_screen(self):
        return self.x > WIDTH


class Player:
    def __init__(self):
        self.x = screen_center[0]
        self.y = screen_center[1]
        self.width = 100
        self.height = 100
        self.speed = 8
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
    
    def hit_by(self, water):
        # 플레이어의 충돌 영역 정의
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # water의 충돌 영역 정의
        water_rect = pygame.Rect(water.x, water.y, 100, 100)
        # 충돌 체크
        return player_rect.colliderect(water_rect)


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
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

clock = pygame.time.Clock()

def mainmenu():
    global menu
    menu = True
    while menu:
        clock.tick(75)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(WHITE)
        menu_text = menu_font.render("벌레 전사는 물이 무서워요", True, BLACK)
        screen.blit(menu_text,(screen_center[0]-600,100))
        startButton = Button(startimg,screen_center[0]-150,screen_center[1]-110,300,200,clickstartimg,mainGame)
        quitButton = Button(quitimg,screen_center[0]-150,screen_center[1]+100,300,200,clickquitimg,quitGame)

        pygame.display.flip()

def mainGame():
    global move, last_raindrop_time, score, menu
    pygame.mixer.music.play(-1)
    timer = 0
    whattime = 0
    menu = False
    players = Player()
    running = True
    while running:
        clock.tick(60)
        screen.blit(backgroundimg,(0,0))

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
            down.append(bulletDown())
            up.append(bulletUp())
            right.append(bulletRight())
            left.append(bulletLeft())
            last_raindrop_time = current_timef

        a=0
        b=0
        c=0
        d=0
        
        while a < len(down):
            down[a].move()
            down[a].draw()
            if players.hit_by(down[a]):
                running = False
                gameOver()
            elif down[a].off_screen():
                del down[a]
                a -= 1
            a += 1
        while b < len(left):
            left[b].move()
            left[b].draw()
            if players.hit_by(left[b]):
                running = False
                gameOver()
            elif left[b].off_screen():
                del left[b]
                b -= 1
            b += 1
        while c < len(up):
            up[c].move()    
            up[c].draw()
            if players.hit_by(up[c]):
                running = False
                gameOver()
            elif up[c].off_screen():
                del up[c]
                c -= 1
            c += 1
        while d < len(right):
            right[d].move()
            right[d].draw()
            if players.hit_by(right[d]):
                running = False
                gameOver()
            elif right[d].off_screen():
                del right[d]
                d -= 1
            d += 1
        
        timer = pygame.time.get_ticks()
        if timer - whattime > 1000:
            score += 1
            whattime = timer

        score_text = score_font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, score_text_position)
        pygame.display.flip()

def gameOver():
    restart = True
    pygame.mixer.music.stop()
    while restart:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(WHITE)
        game_over_text = score_font.render("Game Over", True, BLACK)
        score_text = score_font.render(f"Your Score: {score}", True, BLACK)

        screen.blit(game_over_text, (screen_center[0] - 200, screen_center[1] - 50))
        screen.blit(score_text, (screen_center[0] - 150, screen_center[1] + 50))

        pygame.display.flip()
    
    
mainmenu()