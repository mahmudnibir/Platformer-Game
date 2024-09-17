import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game Shop")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)

# Player Stats
player_coins = 50  # Initial coins
player_health = 100
current_level = 1

# Notification settings
notification = ""  # Empty by default
notification_time = 0  # Time to show the notification

# Functions to draw text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Function to show notifications (for not enough coins)
def show_notification(text):
    global notification, notification_time
    notification = text
    notification_time = pygame.time.get_ticks()  # Get the current time

# Shop menu
def shop_menu():
    global player_coins, player_health, current_level, notification, notification_time

    running = True
    while running:
        screen.fill(WHITE)
        draw_text(f'Coins: {player_coins}', font, BLACK, screen, WIDTH // 2, 50)

        # Shop items (Upgrade health, Skip level)
        draw_text('1. Upgrade Health (10 Coins)', small_font, BLACK, screen, WIDTH // 2, 200)
        draw_text('2. Skip Level (20 Coins)', small_font, BLACK, screen, WIDTH // 2, 300)

        # Check for input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Upgrade health
                    if player_coins >= 10:
                        player_coins -= 10
                        player_health += 20
                        print("Upgraded health! Current health:", player_health)
                    else:
                        show_notification("Not enough coins to upgrade health!")
                if event.key == pygame.K_2:  # Skip level
                    if player_coins >= 20:
                        player_coins -= 20
                        current_level += 1
                        print("Skipped to next level! Current level:", current_level)
                    else:
                        show_notification("Not enough coins to skip level!")

        # Display notification for insufficient coins
        if notification and pygame.time.get_ticks() - notification_time < 2000:  # Show for 2 seconds
            draw_text(notification, small_font, RED, screen, WIDTH // 2, HEIGHT - 50)
        else:
            notification = ""  # Clear notification after 2 seconds

        pygame.display.update()

# Dummy game loop
def game_loop():
    running = True
    while running:
        screen.fill(WHITE)
        draw_text(f'Playing... Coins: {player_coins}', font, BLACK, screen, WIDTH // 2, HEIGHT // 4)

        draw_text('Press "S" to open the shop', small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    shop_menu()  # Open the shop

        pygame.display.update()

# Run the game
game_loop()
