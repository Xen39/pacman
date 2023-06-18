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

    def generate_enemy_list(ctor, num):
        enemy_list = []
        i = 0
        while i < num:
            pos = random_pos(50, 50)
            if distance(pos, pacman.rect.center) < min(HEIGHT, WIDTH) / 3:
                continue
            enemy_list.append(ctor(pos))
            i+=1
        return enemy_list

    random_enemy_list = generate_enemy_list(RandomEnemy, num_random_enemies)
    track_enemy_list = generate_enemy_list(TrackEnemy, num_track_enemies)

    def paint():
        # 渲染游戏画面
        SCREEN.fill(bg_color)

        for obj in food_list + [pacman] + random_enemy_list + track_enemy_list:
            obj.draw_itself(SCREEN)

        # 显示分数
        font = pygame.font.SysFont("Arial", 36)
        num_cur_enemies = len(track_enemy_list) + len(random_enemy_list)
        num_total_enemies = num_track_enemies + num_random_enemies
        tip_text = font.render(f"Score: {pacman.weight * 10} Enemy: {num_cur_enemies}/{num_total_enemies}", True, WHITE)
        SCREEN.blit(tip_text, (10, 10))
        pygame.display.flip()

    def end(tip_word, color):
        # 游戏结束结算页面

        end_time = time.time()

        end_text = pygame.font.SysFont("Arial", 120, bold=True).render(tip_word, True, color)
        end_rect = end_text.get_rect(center=(WIDTH / 2, HEIGHT * 0.3))

        time_text = pygame.font.SysFont("Arial", 50).render(f"Time:  {(end_time - start_time).__round__(3)}s", True, WHITE)
        time_rect = time_text.get_rect(center=(WIDTH / 2, HEIGHT * 0.5))

        score_text = pygame.font.SysFont("Arial", 50).render(f"Score: {pacman.weight * 10}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH / 2, HEIGHT * 0.6))

        exit_text = pygame.font.SysFont("Arial", 50).render("Exit (ESC)", True, WHITE)
        exit_rect = exit_text.get_rect(center=(WIDTH / 2, HEIGHT * 0.75))

        ending = True
        # 游戏结束结算页面主循环
        while ending:
            SCREEN.fill(bg_color)
            SCREEN.blit(end_text, end_rect)
            SCREEN.blit(time_text, time_rect)
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

    def win():
        end("You win!", YELLOW)

    def game_over():
        end("Game over!", RED)

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
                    game_over()
                    return

        paint()

        # 判断是否已经吃掉所有食物
        if len(food_list) == 0:
            running = False

    win()


if __name__ == "__main__":
    run()
