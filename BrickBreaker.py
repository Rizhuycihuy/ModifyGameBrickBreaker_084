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

class Ball:

    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color

        self.xFac, self.yFac = 1, -1

        self.ball = pygame.Rect(
            self.posx - radius,
            self.posy - radius,
            radius * 2,
            radius * 2
        )

    def display(self):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.posx), int(self.posy)),
            self.radius
        )

        self.ball.center = (
            int(self.posx), int(self.posy)
        )

    def update(self):
        self.posx += self.xFac * self.speed
        self.posy += self.yFac * self.speed

        # Left and right wall
        if self.posx - self.radius <= 0:
            self.posx = self.radius
            self.xFac = abs(self.xFac)

        elif self.posx + self.radius >= WIDTH:
            self.posx = WIDTH - self.radius
            self.xFac = -abs(self.xFac)

        # Top wall
        if self.posy - self.radius <= 0:
            self.posy = self.radius
            self.yFac = abs(self.yFac)

        # Bottom wall
        if self.posy - self.radius >= HEIGHT:
            return True

        self.ball.center = (
            int(self.posx), int(self.posy)
        )

        return False

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT - 100

        self.xFac = random.choice([-1, 1])
        self.yFac = -1

        self.ball.center = (
            int(self.posx), int(self.posy)
        )

    def hit(self):
        self.yFac *= -1

    def setSpeed(self, newSpeed):
        self.speed = newSpeed

    def getRect(self):
        self.ball.center = (
            int(self.posx), int(self.posy)
        )

        return self.ball


class Block:

    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color

        self.damage = 100

        if color == WHITE:
            self.health = 200
        else:
            self.health = 100

        self.blockRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height
        )

    def display(self):
        if self.health > 0:
            pygame.draw.rect(
                screen, self.color, self.blockRect
            )

    def hit(self):
        self.health -= self.damage

    def getRect(self):
        return self.blockRect

    def getHealth(self):
        return self.health

class PowerUp:

    def __init__(self, posx, posy, powerType):
        self.posx = posx
        self.posy = posy

        self.powerType = powerType
        self.speed = 4
        self.radius = 12

        self.rect = pygame.Rect(
            posx - self.radius,
            posy - self.radius,
            self.radius * 2,
            self.radius * 2
        )

        self.colors = {
            "wide": BLUE,
            "slow": YELLOW,
            "life": RED
        }

        self.symbols = {
            "wide": "W",
            "slow": "S",
            "life": "+"
        }

    def update(self):
        self.posy += self.speed

        self.rect.center = (
            int(self.posx), int(self.posy)
        )

    def display(self):
        pygame.draw.circle(
            screen,
            self.colors[self.powerType],
            self.rect.center,
            self.radius
        )

        text = font.render(
            self.symbols[self.powerType],
            True,
            BLACK
        )

        screen.blit(
            text,
            text.get_rect(center=self.rect.center)
        )

    def getRect(self):
        return self.rect

def collisionChecker(rect, ball):
    return rect.colliderect(ball)


def populateBlocks(blockWidth, blockHeight,
                  horizontalGap, verticalGap):

    listOfBlocks = []

    for i in range(0, WIDTH, blockWidth + horizontalGap):

        for j in range(0, HEIGHT // 2,
                      blockHeight + verticalGap):

            listOfBlocks.append(
                Block(
                    i, j,
                    blockWidth,
                    blockHeight,
                    random.choice([WHITE, GREEN])
                )
            )

    return listOfBlocks


def gameOver(score):

    while True:

        screen.fill(BLACK)

        title = bigFont.render(
            "GAME OVER", True, RED
        )

        scoreText = font.render(
            "Final Score : " + str(score),
            True, WHITE
        )

        restartText = font.render(
            "Press SPACE to restart",
            True, GREEN
        )

        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, 180)
            )
        )

        screen.blit(
            scoreText,
            scoreText.get_rect(
                center=(WIDTH // 2, 240)
            )
        )

        screen.blit(
            restartText,
            restartText.get_rect(
                center=(WIDTH // 2, 290)
            )
        )

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    return True

        clock.tick(FPS)
