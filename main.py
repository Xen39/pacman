import pygame
import random
import time

from config import *
from food import Food
from pacman import *
from util import *


def run():
    # 初始化 Pygame
    pygame.init()

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(caption)

    # 初始化角色
    pacman = PacMan((WIDTH / 2, HEIGHT / 2))

    food_list = []
    for i in range(num_food):
        food_list.append(Food(random_pos(food_size, food_size)))

    random_enemy_list = []
    for i in range(num_random_enemies):
        random_enemy_list.append(RandomEnemy(random_pos(50, 50)))

    track_enemy_list = []
    for i in range(num_track_enemies):
        track_enemy_list.append(TrackEnemy(random_pos(50, 50)))

    def paint():
        # 渲染游戏画面
        SCREEN.fill(bg_color)

        for obj in food_list + [pacman] + random_enemy_list + track_enemy_list:
            obj.draw_itself(SCREEN)

        # 显示分数
        font = pygame.font.SysFont("Arial", 36)
        text = font.render(f"Score: {pacman.weight * 10}", True, WHITE)
        SCREEN.blit(text, (10, 10))
        pygame.display.flip()

    def end(tip_word):
        # 游戏结束结算页面
        font = pygame.font.SysFont("Arial", 64)

        over_text = font.render(tip_word, True, WHITE)
        over_rect = over_text.get_rect(center=(WIDTH / 2, HEIGHT * 0.3))

        score_text = font.render(f"Score: {pacman.weight}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH / 2, HEIGHT * 0.5))

        exit_text = font.render("Exit (ESC)", True, YELLOW)
        exit_rect = exit_text.get_rect(center=(WIDTH / 2, HEIGHT * 0.8))

        ending = True
        # 游戏结束结算页面主循环
        while ending:
            SCREEN.fill(bg_color)
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

    # 游戏循环
    running = True
    clock = pygame.time.Clock()

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
            if pacman.rect.colliderect(food.rect):
                food_list.remove(food)
                pacman.add_weight(1)

        # enemy
        for enemy in random_enemy_list + track_enemy_list:
            if pacman.rect.colliderect(enemy):
                if pacman.weight_lv() > enemy.weight_lv():
                    if enemy in random_enemy_list:
                        random_enemy_list.remove(enemy)
                    else:
                        track_enemy_list.remove(enemy)
                    pacman.add_weight(enemy.weight)
                else:
                    end_time = time.time()
                    duration = end_time - start_time
                    end('Game over!  cost %.2fs' % duration)
                    return

        paint()

        # 判断是否已经吃掉所有食物
        if len(food_list) == 0:
            running = False

    end_time = time.time()
    duration = end_time - start_time
    end('You win!  cost %.2fs' % duration)


if __name__ == "__main__":
    run()
