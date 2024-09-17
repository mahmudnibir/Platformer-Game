import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Game Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)

# Functions to draw text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Confirmation dialog for quitting
def quit_confirmation():
    while True:
        screen.fill(WHITE)
        draw_text("Are you sure you want to quit?", font, BLACK, screen, WIDTH // 2, HEIGHT // 3)

        # Yes button
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if WIDTH // 2 - 100 <= mouse[0] <= WIDTH // 2 + 100 and HEIGHT // 2 - 25 <= mouse[1] <= HEIGHT // 2 + 25:
            pygame.draw.rect(screen, GREEN, [WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50])
            if click[0] == 1:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(screen, BLACK, [WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50])
        draw_text('Yes', font, WHITE, screen, WIDTH // 2, HEIGHT // 2)

        # No button
        if WIDTH // 2 - 100 <= mouse[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 75 <= mouse[1] <= HEIGHT // 2 + 125:
            pygame.draw.rect(screen, RED, [WIDTH // 2 - 100, HEIGHT // 2 + 75, 200, 50])
            if click[0] == 1:
                return  # Return to the main menu
        else:
            pygame.draw.rect(screen, BLACK, [WIDTH // 2 - 100, HEIGHT // 2 + 75, 200, 50])
        draw_text('No', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 100)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Main menu function
def main_menu():
    while True:
        screen.fill(WHITE)  # Background color
        draw_text('Main Menu', font, BLACK, screen, WIDTH // 2, HEIGHT // 4)

        # Create buttons
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Play Button
        if WIDTH // 2 - 100 <= mouse[0] <= WIDTH // 2 + 100 and HEIGHT // 2 - 25 <= mouse[1] <= HEIGHT // 2 + 25:
            pygame.draw.rect(screen, BLUE, [WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50])
            if click[0] == 1:
                game_loop()  # Start the game loop
        else:
            pygame.draw.rect(screen, BLACK, [WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50])
        draw_text('Play', font, WHITE, screen, WIDTH // 2, HEIGHT // 2)

        # Settings Button
        if WIDTH // 2 - 100 <= mouse[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 75 <= mouse[1] <= HEIGHT // 2 + 125:
            pygame.draw.rect(screen, BLUE, [WIDTH // 2 - 100, HEIGHT // 2 + 75, 200, 50])
            if click[0] == 1:
                print("Settings")  # You can replace this with a settings function
        else:
            pygame.draw.rect(screen, BLACK, [WIDTH // 2 - 100, HEIGHT // 2 + 75, 200, 50])
        draw_text('Settings', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 100)

        # Level Button
        if WIDTH // 2 - 100 <= mouse[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 175 <= mouse[1] <= HEIGHT // 2 + 225:
            pygame.draw.rect(screen, BLUE, [WIDTH // 2 - 100, HEIGHT // 2 + 175, 200, 50])
            if click[0] == 1:
                print("Level Select")  # You can replace this with level selection logic
        else:
            pygame.draw.rect(screen, BLACK, [WIDTH // 2 - 100, HEIGHT // 2 + 175, 200, 50])
        draw_text('Level', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 200)

        # Quit Button
        if WIDTH // 2 - 100 <= mouse[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 275 <= mouse[1] <= HEIGHT // 2 + 325:
            pygame.draw.rect(screen, RED, [WIDTH // 2 - 100, HEIGHT // 2 + 275, 200, 50])
            if click[0] == 1:
                quit_confirmation()  # Show confirmation dialog
        else:
            pygame.draw.rect(screen, BLACK, [WIDTH // 2 - 100, HEIGHT // 2 + 275, 200, 50])
        draw_text('Quit', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 300)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Dummy game loop
def game_loop():
    running = True
    while running:
        screen.fill(WHITE)
        draw_text('Game Running...', font, BLACK, screen, WIDTH // 2, HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

# Run the menu
main_menu()
