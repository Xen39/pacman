import random

from config import *


def random_pos(width, height):
    return random.randint(width, WIDTH - width), random.randint(height, HEIGHT - height)


def distance(pos1, pos2):
    return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5
