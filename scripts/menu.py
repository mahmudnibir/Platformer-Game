import pygame

class Menu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Modern fonts
        self.font = pygame.font.SysFont("Arial", 50)
        self.small_font = pygame.font.SysFont("Arial", 30)
        self.button_size = (220, 60)

        # Colors
        self.button_color = (52, 152, 219)
        self.hover_color = (41, 128, 185)
        self.text_color = (255, 255, 255)
        self.bg_color = (236, 240, 241)
        self.help_bg_color = (44, 62, 80)

        # Main menu buttons
        self.main_buttons = {
            'Play': (self.screen_width // 2, self.screen_height // 2 - 120),
            'Help': (self.screen_width // 2, self.screen_height // 2),
            'Quit': (self.screen_width // 2, self.screen_height // 2 + 120)
        }

        # Level menu buttons
        self.level_buttons = {
            'Level 1': (self.screen_width // 2 - 150, self.screen_height // 2 - 80),
            'Level 2': (self.screen_width // 2 + 150, self.screen_height // 2 - 80),
            'Level 3': (self.screen_width // 2 - 150, self.screen_height // 2 + 40),
            'Level 4': (self.screen_width // 2 + 150, self.screen_height // 2 + 40),
            'Back':    (80, 80)
        }

        # Help menu button
        self.help_buttons = {'Back': (80, 80)}

        self.current_menu = 'main'

    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        self.screen.blit(text_obj, text_rect)

    def draw_button(self, label, x, y, color, hover_color):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x - self.button_size[0] // 2, y - self.button_size[1] // 2, *self.button_size)

        # Button shadow
        shadow_rect = rect.copy()
        shadow_rect.move_ip(3, 3)
        pygame.draw.rect(self.screen, (200, 200, 200), shadow_rect, border_radius=10)

        if rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, hover_color, rect, border_radius=10)
            if click[0] == 1:
                return label
        else:
            pygame.draw.rect(self.screen, color, rect, border_radius=10)

        self.draw_text(label, self.font, self.text_color, x, y)
        return None

    def display_help(self):
        running = True
        while running:
            self.screen.fill(self.help_bg_color)
            self.draw_text('Controls', self.font, (255, 255, 255), self.screen_width // 2, 100)

            # Key bindings in a modern way
            controls = [
                ('Move Right:', '→ Right Arrow'),
                ('Move Left:', '← Left Arrow'),
                ('Jump:', '↑ Up Arrow'),
                ('Shoot:', 'Spacebar'),
                ('Throw Grenade:', 'Shift')
            ]
            
            for i, (action, key) in enumerate(controls):
                self.draw_text(f'{action} {key}', self.small_font, (255, 255, 255),
                               self.screen_width // 2, 200 + i * 50)
            
            back_button = self.draw_button('Back', self.help_buttons['Back'][0], self.help_buttons['Back'][1],
                                           self.button_color, self.hover_color)
            if back_button == 'Back':
                self.current_menu = 'main'
                return None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            pygame.display.update()

    def level_menu(self):
        while True:
            self.screen.fill(self.bg_color)
            self.draw_text('Select Level', self.font, (44, 62, 80), self.screen_width // 2, self.screen_height // 4)

            for label, (x, y) in self.level_buttons.items():
                selected_button = self.draw_button(label, x, y, self.button_color, self.hover_color)
                if selected_button:
                    if selected_button == 'Back':
                        self.current_menu = 'main'
                        return None
                    return selected_button

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            pygame.display.update()

    def run(self):
        while True:
            self.screen.fill(self.bg_color)

            if self.current_menu == 'main':
                for label, (x, y) in self.main_buttons.items():
                    selected_button = self.draw_button(label, x, y, self.button_color, self.hover_color)
                    if selected_button:
                        if selected_button == 'Play':
                            self.current_menu = 'levels'
                            return None
                        elif selected_button == 'Help':
                            self.display_help()
                        elif selected_button == 'Quit':
                            pygame.quit()
                            return

            elif self.current_menu == 'levels':
                selected_level = self.level_menu()
                if selected_level:
                    return selected_level

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            pygame.display.update()
