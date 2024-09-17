import pygame
import os
import buttons
import csv
import pickle

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# game window
SCREEN_WIDTH = 740
SCREEN_HEIGHT = 600
LOWER_MARGIN = 100
SIDE_MARGIN = 280

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

# define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
scrollbar_dragging = False

bg_img = pygame.image.load('assets/images/bg_image/background.png').convert_alpha()

# Load tile names from the image files in the directory
tile_names = []
tile_images = []
tile_dir = 'assets/images/tile/'

for filename in os.listdir(tile_dir):
    if filename.endswith('.png'):
        tile_name = os.path.splitext(filename)[0]
        tile_names.append(tile_name)
        img = pygame.image.load(os.path.join(tile_dir, filename)).convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        tile_images.append(img)

save_img = pygame.image.load('assets/images/button_image/save_btn.png').convert_alpha()
load_img = pygame.image.load('assets/images/button_image/load_btn.png').convert_alpha()

# define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
SCROLLBAR_COLOR = (150, 150, 150)
SCROLLBAR_BG = (50, 50, 50)

# define font
font = pygame.font.SysFont('Futura', 30)
font_small = pygame.font.SysFont('Futura', 16)

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0

# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# create function for drawing background
def draw_bg():
    screen.fill(GREEN)
    width = bg_img.get_width()
    for x in range(4):
        screen.blit(bg_img, ((x * width) - scroll * 0.5, 0))

# draw grid
def draw_grid():
    # vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    # horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

# function for drawing the world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(tile_images[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

# create buttons
save_button = buttons.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = buttons.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

# make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(tile_images)):
    tile_button = buttons.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 10, tile_images[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:  # Switch back to three columns
        button_row += 1
        button_col = 0

# Add scroll offset for side panel
side_panel_scroll = 0
side_panel_scroll_speed = 10
max_scroll = max(0, (len(tile_images) // 3) * 75 - SCREEN_HEIGHT)  # Adjust based on the number of rows of buttons

# Function to draw the tile panel with scrolling and a scrollbar
# Function to draw the tile panel with scrolling and a scrollbar
def draw_tile_panel():
    # Draw the side margin background
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))

    # Draw the buttons with scrolling
    for button_count, i in enumerate(button_list):
        # Temporarily move the rect for drawing and selection based on the scroll
        i.rect.y -= side_panel_scroll
        # Draw only buttons that are visible on the screen
        if 0 <= i.rect.y <= SCREEN_HEIGHT + LOWER_MARGIN:
            i.draw(screen)
            # Highlight the selected tile
            if current_tile == button_count:
                pygame.draw.rect(screen, RED, i.rect, 3)
            # Draw tile names
            if button_count < len(tile_names):
                text_x = i.rect.x + (TILE_SIZE // 2) - font_small.size(tile_names[button_count])[0] // 2
                text_y = i.rect.y + TILE_SIZE + 2
                draw_text(tile_names[button_count], font_small, WHITE, text_x, text_y)
        # Reset the button rect position after drawing
        i.rect.y += side_panel_scroll

    # Draw scrollbar background
    scrollbar_height = SCREEN_HEIGHT + LOWER_MARGIN
    scrollbar_width = 15
    pygame.draw.rect(screen, SCROLLBAR_BG, (SCREEN_WIDTH + SIDE_MARGIN - scrollbar_width, 0, scrollbar_width, scrollbar_height))

    if max_scroll > 0:  # Only draw the scrollbar handle if scrolling is needed
        # Calculate handle height and position
        handle_height = max(40, int(SCREEN_HEIGHT * (SCREEN_HEIGHT / (max_scroll + SCREEN_HEIGHT))))
        handle_pos = int((side_panel_scroll / max_scroll) * (scrollbar_height - handle_height))
        pygame.draw.rect(screen, SCROLLBAR_COLOR, (SCREEN_WIDTH + SIDE_MARGIN - scrollbar_width, handle_pos, scrollbar_width, handle_height))


run = True
while run:
    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # save and load data
    if save_button.draw(screen):
        # save level data
        with open(f'data/level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)

    if load_button.draw(screen):
        # load in level data
        # reset scroll back to the start of the level
        scroll = 0
        with open(f'data/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    # Handle scrolling the side panel with mouse wheel and arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        side_panel_scroll = min(max_scroll, side_panel_scroll + side_panel_scroll_speed)
    if keys[pygame.K_UP]:
        side_panel_scroll = max(0, side_panel_scroll - side_panel_scroll_speed)

    for event in pygame.event.get():
     if event.type == pygame.QUIT:
          run = False

     # Handle mouse events for dragging the scrollbar
     if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
               mouse_x, mouse_y = event.pos
               scrollbar_rect = pygame.Rect(SCREEN_WIDTH + SIDE_MARGIN - 15, 0, 15, SCREEN_HEIGHT + LOWER_MARGIN)
               if max_scroll > 0 and scrollbar_rect.collidepoint(mouse_x, mouse_y):
                    handle_height = max(40, int(SCREEN_HEIGHT * (SCREEN_HEIGHT / (max_scroll + SCREEN_HEIGHT))))
                    handle_pos = int((side_panel_scroll / max_scroll) * (SCREEN_HEIGHT + LOWER_MARGIN - handle_height))
                    handle_rect = pygame.Rect(SCREEN_WIDTH + SIDE_MARGIN - 15, handle_pos, 15, handle_height)
                    if handle_rect.collidepoint(mouse_x, mouse_y):
                         scrollbar_dragging = True
                         drag_offset = mouse_y - handle_pos

     if event.type == pygame.MOUSEBUTTONUP:
          scrollbar_dragging = False

     if event.type == pygame.MOUSEMOTION:
          if scrollbar_dragging:
               mouse_x, mouse_y = event.pos
               if max_scroll > 0:
                    handle_height = max(40, int(SCREEN_HEIGHT * (SCREEN_HEIGHT / (max_scroll + SCREEN_HEIGHT))))
                    new_handle_pos = mouse_y - drag_offset
                    side_panel_scroll = int((new_handle_pos / (SCREEN_HEIGHT + LOWER_MARGIN - handle_height)) * max_scroll)
                    side_panel_scroll = max(0, min(max_scroll, side_panel_scroll))

     # Mouse scrolling
     if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 4:  # Scroll up
               side_panel_scroll = max(0, side_panel_scroll - side_panel_scroll_speed)
          if event.button == 5:  # Scroll down
               side_panel_scroll = min(max_scroll, side_panel_scroll + side_panel_scroll_speed)
               
     pos = pygame.mouse.get_pos()
     x = (pos[0] + scroll) // TILE_SIZE
     y = pos[1] // TILE_SIZE

     if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
          if pygame.mouse.get_pressed()[0] == 1:  # Left click
               if 0 <= x < MAX_COLS and 0 <= y < ROWS:
                    if world_data[y][x] != current_tile:
                         world_data[y][x] = current_tile
          if pygame.mouse.get_pressed()[2] == 1:  # Right click
               if 0 <= x < MAX_COLS and 0 <= y < ROWS:
                    world_data[y][x] = -1



    # Draw the tile panel with the scrollbar and names
    draw_tile_panel()

    pygame.display.update()

pygame.quit()
