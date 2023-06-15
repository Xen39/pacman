import random

from config import *


def random_pos(width, height):
    return random.randint(width, WIDTH - width), random.randint(height, HEIGHT - height)
