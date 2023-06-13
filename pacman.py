import pygame
import random

from config import *


class Direction:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]


class Man:
    def __init__(self, pos, image_name, speed=default_speed/FPS, weight=0):
        self.origin_image = self.image = pygame.image.load(image_name)
        self.speed = speed
        assert speed > 0.5, f"speed设置过小({speed * FPS})"
        self.weight = 0
        self.rect = self.curr_image().get_rect()
        self.rect.center = pos
        self.add_weight(weight)
        self.direction = Direction((0, 0))

    def curr_image(self):
        return self.image

    def _unsafe_move(self):
        self.rect.centerx += self.direction.x * self.speed
        self.rect.centery += self.direction.y * self.speed

    def _safe_move(self):
        self._unsafe_move()
        # 检查是否碰到边界
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def tick(self):
        self._safe_move()

    def weight_lv(self):
        return self.weight**0.8//10

    def add_weight(self, w):
        weight_lv1 = self.weight_lv()
        self.weight += w
        weight_lv2 = self.weight_lv()
        if weight_lv2 != weight_lv1:
            self.image = pygame.transform.rotozoom(self.origin_image, 0, 1 + weight_lv2/10)
            center = self.rect.center
            self.rect = self.curr_image().get_rect()
            self.rect.center = center

    @staticmethod
    def random_direction():
        return Direction(random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)]))


class PacMan(Man):
    def __init__(self, pos):
        super().__init__(pos, pacman_img_name)

    def keyboard_rotate(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction.x = -1
            elif event.key == pygame.K_RIGHT:
                self.direction.x = 1
            elif event.key == pygame.K_UP:
                self.direction.y = -1
            elif event.key == pygame.K_DOWN:
                self.direction.y = 1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.direction.x += 1
            if event.key == pygame.K_RIGHT:
                self.direction.x -= 1
            elif event.key == pygame.K_UP:
                self.direction.y += 1
            elif event.key == pygame.K_DOWN:
                self.direction.y -= 1

        def limit_to_range(num, min, max):
            if num < min:
                return min
            elif num > max:
                return max
            return num

        self.direction.x = limit_to_range(self.direction.x, -1, 1)
        self.direction.y = limit_to_range(self.direction.y, -1, 1)


class RandomEnemy(Man):
    def __init__(self, pos):
        super().__init__(pos, random_enemy_img_name, weight=random.randint(num_food/10, num_food))
        self.direction = Man.random_direction()

    def random_rotate(self):
        def hit_wall():
            return (self.rect.top <= 0 and self.direction.y < 0) \
                or (self.rect.bottom >= HEIGHT and self.direction.y > 0) \
                or (self.rect.left <= 0 and self.direction.x < 0) \
                or (self.rect.right >= WIDTH and self.direction.x > 0)

        if random.random() < 0.02:
            self.direction = Direction(random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)]))
        while hit_wall():
            self.direction = Direction(random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)]))


class TrackEnemy(Man):
    def __init__(self, pos):
        super().__init__(pos, track_enemy_img_name, weight=random.randint(num_food/10, num_food))
        self.direction = Man.random_direction()

    def track_rotate(self, pos):
        assert self.direction.x * self.direction.y == 0
        # 如果原运动方向可以继续接近pos, 保持原方向
        if self.direction.x * (pos[0] - self.rect.centerx) > 0:
            return
        if self.direction.y * (pos[1] - self.rect.centery) > 0:
            return
        if self.direction.x == 0 and self.direction.y == 0:
            if pos[1] != self.rect.centery:
                self.direction.y = 1 if pos[1] - self.rect.centery > 0 else -1
            elif pos[0] != self.rect.centerx:
                self.direction.x = 1 if pos[0] - self.rect.centerx > 0 else -1
            return

        if self.direction.x != 0:  # 原来静止和横向移动的优先竖向移动
            if pos[1] != self.rect.centery:
                self.direction.x = 0
                self.direction.y = 1 if pos[1] - self.rect.centery > 0 else -1
            else:
                self.direction.x *= -1
            return

        else:
            if pos[0] != self.rect.centerx:
                self.direction.x = 1 if pos[0] - self.rect.centerx > 0 else -1
                self.direction.y = 0
            else:
                self.direction.y *= -1
            return
