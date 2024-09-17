import pygame
import math

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

# Load the image
heart_image = pygame.image.load('assets/images/resources/heart.png')
heart_image.set_colorkey((0, 0, 0))  # Ensure the heart image background is transparent

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        self.font = pygame.font.SysFont(None, 24)
        self.image_size = 20  # Desired size of the heart image (width and height)
        self.beat_speed = 0.005  # Slower speed for the beating effect

    def draw(self, health):
        # Update with new health
        self.health = health
        # Calculate health ratio
        ratio = self.health / self.max_health

        # Calculate color transition from green to red
        green_to_red = (255 - int(255 * ratio), int(255 * ratio), 0)

        # Calculate beating effect
        time = pygame.time.get_ticks()
        beat_size = int(self.image_size + 5 * math.sin(time * self.beat_speed))  # Pulsing effect

        # Resize the heart image
        heart_image_resized = pygame.transform.scale(heart_image, (beat_size, beat_size))

        # Draw background
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154 + self.image_size, 24))

        # Draw health bar background (black bar)
        pygame.draw.rect(screen, BLACK, (self.x + self.image_size, self.y, 150, 20))

        # Draw the health bar with gradient from green to red
        pygame.draw.rect(screen, green_to_red, (self.x + self.image_size, self.y, 150 * ratio, 20))

        # Draw the heart image on the left side of the health bar, outside the box
        heart_x = self.x - (beat_size - self.image_size) // 2
        heart_y = self.y + 2 - beat_size // 2
        screen.blit(heart_image_resized, (heart_x, heart_y+4))

        # Draw health text
        text = self.font.render(f'Health: {self.health}', True, WHITE)
        screen.blit(text, (self.x + self.image_size + 19, self.y + 2))
