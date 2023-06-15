import pygame

from config import *
import util


class Food:
    def __init__(self, pos=None):
        if pos is None:
            pos = util.random_pos(food_size, food_size)
        self.rect = pygame.Rect(pos[0], pos[1], food_size, food_size)

    def draw_itself(self, screen):
        pygame.draw.rect(screen, food_color, self.rect)
