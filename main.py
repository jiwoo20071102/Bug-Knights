import pygame
import random as rd
import sys

# 초기화
pygame.init()

# 초기 화면 설정 (비율 유지)
BASE_WIDTH, BASE_HEIGHT = 800, 600
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("벌레전사의 바다모험기")

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TRANSLUCENT_RED = (255, 0, 0, 64)  # 빨간색 반투명 (25% 투명도)

# 한글 폰트 로드
font_path = 'Resource/Fonts/jua.ttf'  # 여기에 jua.ttf 경로
title_font = pygame.font.Font(font_path, 80)
subtitle_font = pygame.font.Font(font_path, 40)
option_font = pygame.font.Font(font_path, 30)

# 리소스 불러오기
background = pygame.image.load('Resource/Ui/background.png')

# 플레이어 이미지 로드
player_images = {
    "down": pygame.image.load('Resource/PlayerMovement/player_0.png'),
    "left": pygame.image.load('Resource/PlayerMovement/player_3.png'),
    "right": pygame.image.load('Resource/PlayerMovement/player_1.png'),
    "up": pygame.image.load('Resource/PlayerMovement/player_2.png')
}

# 몬스터 이미지 로드
enemy_idle = pygame.image.load('Resource/PlayerMovement/idle.png')
enemy_move = [
    pygame.image.load('Resource/PlayerMovement/move_1.png'),
    pygame.image.load('Resource/PlayerMovement/move_2.png')
]

# 상태 변수
game_started = False
in_settings = False  # 설정 화면 상태
invincible_time_after_start = 2000  # 게임 시작 후 2초 무적 시간

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_images["down"]
        self.rect = self.image.get_rect(center=(BASE_WIDTH//2, BASE_HEIGHT//2))
        self.speed = 5
        self.direction = "down"
        self.max_hp = 100
        self.hp = self.max_hp
        self.invincible_time = 0  # 무적 상태 시간
        self.invincible_duration = 2000  # 무적 지속 시간 (2초)
        self.blink_time = 0  # 깜빡임 시간
        self.blink_duration = 500  # 500ms마다 깜빡이기

    def update(self, keys):
        if self.invincible_time > 0:
            # 무적 상태라면 시간 감소
            self.invincible_time -= clock.get_time()

        if self.blink_time > 0:
            # 깜빡임 효과
            self.blink_time -= clock.get_time()
            if self.blink_time % 100 < 50:  # 50ms 동안 보이지 않음, 50ms 동안 보임
                self.blink_alpha = 64  # 더 투명하게 설정
            else:
                self.blink_alpha = 255  # 완전 불투명
        else:
            self.blink_alpha = 255  # 깜빡임이 없으면 불투명

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = "right"
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = "up"
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = "down"

        # 방향에 따라 이미지 변경
        self.image = player_images[self.direction]

        # 화면 밖으로 못 나가게
        self.rect.clamp_ip(screen.get_rect())

    def is_invincible(self):
        return self.invincible_time > 0

    def take_damage(self, amount):
        if not self.is_invincible():
            self.hp -= amount
            self.invincible_time = self.invincible_duration  # 무적 상태로 설정
            self.blink_time = 2000  # 깜빡임 시작
            if self.hp < 0:
                self.hp = 0

# 몬스터 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = enemy_move
        self.idle_image = enemy_idle
        self.current_image = 0
        self.image = self.idle_image
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_timer = 0
        self.animation_speed = 200  # 200ms마다 프레임 교체
        self.speed = 2

    def update(self):
        # 랜덤 이동
        self.rect.x += rd.choice([-1, 0, 1]) * self.speed
        self.rect.y += rd.choice([-1, 0, 1]) * self.speed

        # 애니메이션 업데이트
        now = pygame.time.get_ticks()
        if now - self.animation_timer > self.animation_speed:
            self.animation_timer = now
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]

        # 화면 밖으로 못 나가게
        self.rect.clamp_ip(screen.get_rect())

# 체력바 그리기 함수
def draw_health_bar(surface, x, y, current_hp, max_hp):
    BAR_WIDTH = 200
    BAR_HEIGHT = 20
    fill = (current_hp / max_hp) * BAR_WIDTH
    outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)

    # 체력에 따라 색상 변경
    if current_hp > 20:
        bar_color = GREEN  # 초록색
    else:
        bar_color = RED  # 빨간색

    pygame.draw.rect(surface, bar_color, fill_rect)  # 체력바 채우기
    pygame.draw.rect(surface, (0, 0, 0), outline_rect, 2)  # 테두리

# 화면 주변 빨갛게 반투명 처리
def draw_red_overlay(surface):
    if player.hp <= 20:
        overlay = pygame.Surface((BASE_WIDTH, BASE_HEIGHT), pygame.SRCALPHA)
        overlay.fill(TRANSLUCENT_RED)  # 25% 투명도로 설정
        surface.blit(overlay, (0, 0))

# 스프라이트 그룹
player = Player()
player_group = pygame.sprite.Group(player)

enemy_group = pygame.sprite.Group()
for _ in range(5):  # 몬스터 5마리 생성
    enemy = Enemy(rd.randint(50, BASE_WIDTH-50), rd.randint(50, BASE_HEIGHT-50))
    enemy_group.add(enemy)

# 시작 화면 그리기
def draw_start_screen():
    screen.fill(WHITE)

    title_text = title_font.render("벌레전사의 바다모험기", True, BLACK)
    title_rect = title_text.get_rect(center=(BASE_WIDTH//2, BASE_HEIGHT//3))
    screen.blit(title_text, title_rect)

    now = pygame.time.get_ticks()
    if (now // 500) % 2 == 0:
        subtitle_text = subtitle_font.render("게임 시작 버튼을 클릭하세요", True, BLACK)
        subtitle_rect = subtitle_text.get_rect(center=(BASE_WIDTH//2, BASE_HEIGHT//1.5))
        screen.blit(subtitle_text, subtitle_rect)

    # 게임 시작 버튼
    start_button = pygame.Rect(BASE_WIDTH//3, BASE_HEIGHT//2, BASE_WIDTH//3, 60)
    pygame.draw.rect(screen, GREEN, start_button)
    start_text = option_font.render("게임 시작", True, WHITE)
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

    return start_button

# 게임 화면 그리기
def draw_game_screen():
    keys = pygame.key.get_pressed()
    player.update(keys)
    enemy_group.update()

    # 충돌 체크
    hits = pygame.sprite.spritecollide(player, enemy_group, False)
    for hit in hits:
        if not player.is_invincible():  # 무적 상태가 아닐 때만 피해를 입음
            player.take_damage(20)  # 맞을 때마다 20 깎임

    screen.blit(background, (0, 0))
    
    # 깜빡임 효과 적용 후 플레이어 그리기
    player_image_with_alpha = player.image.copy()
    player_image_with_alpha.set_alpha(player.blink_alpha)  # 알파값 적용
    screen.blit(player_image_with_alpha, player.rect)

    enemy_group.draw(screen)

    # 체력바 그리기 (오른쪽 상단)
    draw_health_bar(screen, BASE_WIDTH - 220, 20, player.hp, player.max_hp)

    # 체력이 20 이하일 때 화면 주변 빨갛게 물들게
    draw_red_overlay(screen)

# 설정 화면 그리기
def draw_settings_screen():
    screen.fill(WHITE)

    title_text = title_font.render("설정", True, BLACK)
    title_rect = title_text.get_rect(center=(BASE_WIDTH//2, BASE_HEIGHT//3))
    screen.blit(title_text, title_rect)

    resume_text = option_font.render("게임 계속하기 (ESC)", True, BLACK)
    resume_rect = resume_text.get_rect(center=(BASE_WIDTH//2, BASE_HEIGHT//2))
    screen.blit(resume_text, resume_rect)

    # "시작 화면으로 돌아가기" 버튼 추가
    restart_text = option_font.render("시작 화면으로 돌아가기", True, BLACK)
    restart_rect = restart_text.get_rect(center=(BASE_WIDTH//2, BASE_HEIGHT//1.5))
    pygame.draw.rect(screen, (200, 200, 200), restart_rect)  # 버튼 배경색
    screen.blit(restart_text, restart_rect)

    return restart_rect

# 마우스 클릭 이벤트 처리
def handle_mouse_click(event, start_button, restart_rect):
    global game_started, in_settings
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse_pos) and not game_started:  # 게임 시작 버튼 클릭
            game_started = True
        elif restart_rect.collidepoint(mouse_pos):  # 시작 화면으로 돌아가기 버튼 클릭
            reset_game()  # 게임 리셋
            in_settings = False  # 설정 화면 종료

# 게임 초기화
def reset_game():
    global game_started, player, enemy_group
    game_started = False
    player = Player()
    player_group = pygame.sprite.Group(player)
    enemy_group = pygame.sprite.Group()
    for _ in range(5):  # 몬스터 5마리 생성
        enemy = Enemy(rd.randint(50, BASE_WIDTH-50), rd.randint(50, BASE_HEIGHT-50))
        enemy_group.add(enemy)

# 메인 루프
def main():
    global game_started, in_settings

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC로 설정 화면
                    in_settings = True

            # 마우스 클릭 이벤트 처리
            if in_settings:
                restart_rect = draw_settings_screen()
                handle_mouse_click(event, None, restart_rect)
            elif not game_started:
                start_button = draw_start_screen()
                handle_mouse_click(event, start_button, None)
            else:
                draw_game_screen()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
