import random

import pygame
from functions import check_limits


class Node:
    VEL = 6
    WIDTH = VEL*2
    HEIGHT = VEL*2
    COLOR = (255, 0, 0)

    def __init__(self, parent=None):
        self.parent = parent
        self.is_head = True
        self.direction = 'right'
        if self.parent:
            self.is_head = False  # is the node has a parent, then it is not the head of the snake

        try:
            """
            These if statement are used to set the child node in the right place
            """
            if self.parent.direction == 'right':
                self.rect = pygame.Rect(self.parent.rect.x - self.WIDTH, self.parent.rect.y, self.WIDTH, self.HEIGHT)

            elif self.parent.direction == 'left':
                self.rect = pygame.Rect(self.parent.rect.x + self.WIDTH, self.parent.rect.y, self.WIDTH, self.HEIGHT)
            elif self.parent.direction == 'up':
                self.rect = pygame.Rect(self.parent.rect.x, self.rect.y - self.HEIGHT, self.WIDTH, self.HEIGHT)
            elif self.parent.direction == 'down':
                self.rect = pygame.Rect(self.parent.rect.x, self.parent.rect.y + self.HEIGHT, self.WIDTH, self.HEIGHT)
            self.direction = self.parent.direction
        except AttributeError:  # in case the object is the head, it means it has no parent
            self.rect = pygame.Rect(self.WIDTH, self.HEIGHT, self.WIDTH, self.HEIGHT)
        self.right = [self.rect.x, self.VEL]
        self.left = [self.rect.x, -self.VEL]
        self.up = [self.rect.y, -self.VEL]
        self.down = [self.rect.y, +self.VEL]
        self.out_of_screen = False

        self.last_change_direction_x_coordinate = self.rect.x
        self.last_change_direction_y_coordinate = self.rect.y

        self.directions = {"left": self.left, "right": self.right, "up": self.up, "down": self.down}

    @check_limits
    def move(self, windows):

        if self.direction == 'right' or self.direction == 'left':
            self.rect.x += self.directions[self.direction][1]
        else:
            self.rect.y += self.directions[self.direction][1]

    def update(self, windows):
        pygame.draw.rect(windows, self.COLOR, self.rect)


class Snake:
    def __init__(self, head: Node):
        self.head = head
        self.nodes = [self.head]


class CheckPoint:
    WIDTH = 20
    HEIGHT = 20

    def __init__(self):
        from main import WINDOWS
        self.rect = pygame.Rect(random.choice(range(WINDOWS.get_width() - 5)),
                                random.choice(range(WINDOWS.get_height() - 5)),
                                self.WIDTH, self.HEIGHT)

        self.image = pygame.transform.scale(pygame.image.load('red_circle.jpg'), (self.WIDTH, self.HEIGHT))


class BigCheckPoint(CheckPoint):
    WIDTH = 50
    HEIGHT = 50

    def __init__(self):
        super().__init__()


class Button:
    def __init__(self, x, y, width, height, text, color, func):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.command = func

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event, *args):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.command(*args)
                return True
        return False


class Label:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
