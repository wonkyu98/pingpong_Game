import pygame
from pygame.locals import *
import sys
import time

# 화면 크기 설정
WIDTH = 640
HEIGHT = 480

# 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 패들 초기 위치 설정
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 10
paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = HEIGHT - PADDLE_HEIGHT - 10

# 공 초기 위치 설정
BALL_RADIUS = 5
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 4
ball_dy = 4

# 점수 초기화
score = 0

# 게임 기회 초기화
chances = 3

# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('1인용 핑퐁 게임 - 이원규')

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

playing = False  # 게임 진행 여부

# 공 속도 설정
def set_ball_speed():
    global ball_dx, ball_dy
    if chances == 3:
        ball_dx = 4
        ball_dy = 4
    elif chances == 2:
        ball_dx = 5
        ball_dy = 5
    elif chances == 1:
        ball_dx = 6
        ball_dy = 6

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if not playing:  # 게임이 진행 중이 아닐 때
        keys = pygame.key.get_pressed()
        if keys[K_SPACE] and chances > 0:  # 스페이스바를 누르면 게임 시작 (기회가 남아있을 경우에만)
            playing = True
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            set_ball_speed()

    if playing:  # 게임이 진행 중일 때
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and paddle_x > 0:
            paddle_x -= 5
        if keys[K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += 5

        # 공 이동
        ball_x += ball_dx
        ball_y += ball_dy

        # 벽과 충돌 검사
        if ball_x <= BALL_RADIUS or ball_x >= WIDTH - BALL_RADIUS:
            ball_dx *= -1
        if ball_y <= BALL_RADIUS:
            ball_dy *= -1

        # 패들과 충돌 검사
        if paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH and ball_y >= paddle_y - BALL_RADIUS:
            ball_dy *= -1
            score += 1

        # 공이 패들을 지나갔을 때 게임 종료
        if ball_y > HEIGHT:
            playing = False
            chances -= 1
            set_ball_speed()

    # 화면 업데이트
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

    # 점수 및 게임 기회 표시
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))
    chances_text = font.render("Chances: " + str(chances), True, WHITE)
    screen.blit(chances_text, (WIDTH - chances_text.get_width() - 10, 10))

    # 게임 종료 조건 체크
    if chances == 0:
        gameover_text = font.render("Game Over", True, WHITE)
        screen.blit(gameover_text, (WIDTH // 2 - gameover_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        time.sleep(3)  # 3초 대기
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(60)