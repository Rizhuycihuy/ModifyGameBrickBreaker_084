import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 600, 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 220, 0)

font = pygame.font.Font('freesansbold.ttf', 15)
bigFont = pygame.font.Font('freesansbold.ttf', 35)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker")

clock = pygame.time.Clock()
FPS = 30

class Striker:

    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.originalWidth = width
        self.speed = speed
        self.color = color

        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

    def display(self):
        pygame.draw.rect(
            screen, self.color, self.strikerRect
        )

    def update(self, xFac):
        self.posx += self.speed * xFac

        if self.posx <= 0:
            self.posx = 0

        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width

        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

    def changeWidth(self, newWidth):
        center = self.strikerRect.centerx

        self.width = newWidth
        self.posx = center - self.width // 2

        self.posx = max(
            0, min(self.posx, WIDTH - self.width)
        )

        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

    def getRect(self):
        return self.strikerRect