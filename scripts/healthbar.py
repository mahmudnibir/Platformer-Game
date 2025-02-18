import pygame

# Initialize Pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        self.font = pygame.font.SysFont(None, 24)


    def draw(self, health):
        # Update with new health
        self.health = health
        # Calculate health ratio
        ratio = self.health / self.max_health

        # Calculate color transition from green to red (convert to integers)
        green_to_red = (255 - int(255 * ratio), int(255 * ratio), 0)

        # Draw background
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))

        # Draw health bar background (black bar)
        pygame.draw.rect(screen, BLACK, (self.x , self.y, 150, 20))

        # Draw the health bar with gradient from green to red
        pygame.draw.rect(screen, green_to_red, (self.x , self.y, 150 * ratio, 20))


        # Draw health text
        text = self.font.render(f'Health: {self.health}', True, WHITE)
        screen.blit(text, (self.x + 19, self.y + 2))

