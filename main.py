import pygame
import random
import time
from pacman import *
from util import *

# 游戏颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BG_COLOR = (80, 80, 80)

food_color_list = (RED)

food_size = 3


def run(num_food, num_random_enemies, num_track_enemies):
    # 初始化 Pygame
    pygame.init()

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PacMan")

    # 游戏速度
    FPS = 30

    # 初始化角色和食物
    pacman = PacMan((WIDTH / 2, HEIGHT / 2), image_name="pacman_left.png")

    # 保留偏移，防止一开始就半张图卡在框外
    save_offset = 10

    def random_pos():
        return random.randint(save_offset, WIDTH - save_offset), random.randint(save_offset, HEIGHT - save_offset)

    food_list = []
    for i in range(num_food):
        pos = random_pos()
        food_list.append(pygame.Rect(pos[0], pos[1], food_size, food_size))

    random_enemy_list = []
    for i in range(num_random_enemies):
        pos = random_pos()
        random_enemy_list.append(PacMan(pos, "ghost.png"))

    track_enemy_list = []
    for i in range(num_track_enemies):
        pos = random_pos()
        track_enemy_list.append(PacMan(pos, "ghost.png"))

    # 显示分数
    score = 0
    font = pygame.font.SysFont("Arial", 36)
    text = font.render("Score: " + str(score), True, WHITE)

    # 游戏循环
    running = True
    clock = pygame.time.Clock()

    def paint():
        # 渲染游戏画面
        SCREEN.fill(BG_COLOR)
        for food in food_list:
            pygame.draw.rect(SCREEN, WHITE, food)

        SCREEN.blit(pacman.curr_image(), pacman.rect)
        for enemy in random_enemy_list + track_enemy_list:
            SCREEN.blit(enemy.curr_image(), enemy.rect)
        SCREEN.blit(text, (10, 10))
        pygame.display.flip()

    def end(tip_word):
        # 游戏结束结算页面
        font = pygame.font.SysFont("Arial", 64)
        over_text = font.render(tip_word, True, WHITE)
        over_rect = over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))

        score_text = font.render("Score: " + str(score), True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))

        exit_text = font.render("Exit (ESC)", True, YELLOW)
        exit_rect = exit_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 200))

        ending = True
        # 游戏结束结算页面主循环
        while ending:
            SCREEN.fill(BG_COLOR)
            SCREEN.blit(over_text, over_rect)
            SCREEN.blit(score_text, score_rect)
            SCREEN.blit(exit_text, exit_rect)
            pygame.display.flip()

            # 处理事件（退出、重新开始）
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    # 关闭 Pygame
                    pygame.quit()
                    ending = False
                    break

    paint()

    # 开始时暂停1s，让玩家有反应时间
    time.sleep(1)
    start_time = time.time()
    while running:
        # 限制游戏运行速度
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            pacman.keyboard_rotate(event)

        for enemy in random_enemy_list:
            enemy.random_rotate()

        for enemy in track_enemy_list:
            enemy.track_rotate((pacman.rect.x, pacman.rect.y))

        for man in [pacman] + random_enemy_list + track_enemy_list:
            man.tick()

        # food
        for food in food_list:
            if pacman.rect.colliderect(food):
                food_list.remove(food)
                score += 10
                text = font.render(f"Score: {score}", True, WHITE)

        # enemy
        for enemy in random_enemy_list + track_enemy_list:
            if pacman.rect.colliderect(enemy):
                end_time = time.time()
                duration = end_time - start_time
                end('Game over!  cost %.2fs'%duration)

                print()
                return

        paint()

        # 判断是否已经吃掉所有食物
        if len(food_list) == 0:
            running = False

    end_time = time.time()
    duration = end_time - start_time
    end('You win!  cost %.2fs' % duration)


# 食物数量
num_food = 1
# 随机移动敌人数量
num_random_enemies = 3
# 自动追踪敌人数量
num_track_enemies = 1

run(num_food, num_random_enemies, num_track_enemies)