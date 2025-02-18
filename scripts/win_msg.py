import pygame
import random

class WinScreen:
    def __init__(self, screen, font, return_to_menu):
        self.screen = screen
        self.font = font
        self.message = "Game Completed!"
        self.info_message = "Press ENTER to return to the Main Menu"
        self.color = (243, 133, 24)
        self.particles = []
        self.music_played = False
        self.return_to_menu = return_to_menu  # Callback to return to main menu
        self.alpha = 0  # For fade-in text effect
        self.fade_in_speed = 3  # Adjust for how fast text fades in

    def play_music(self):
        if not self.music_played:
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.2)
            self.music_played = True

    def add_particles(self):
        # Create particles with additional properties for smooth motion and fading
        for _ in range(5):  # Fewer particles per frame for smoother look
            x = random.randint(0, self.screen.get_width())
            y = self.screen.get_height() + 10  # Start just below the screen
            speed = random.uniform(1, 3)
            size = random.randint(3, 6)
            # Each particle: [x, y, speed, size, alpha]
            self.particles.append([x, y, speed, size, 255])

    def update_particles(self):
        for particle in self.particles:
            # Move upward based on speed
            particle[1] -= particle[2]
            # Gradually fade out by reducing alpha
            particle[4] -= 3  
            # Optionally shrink over time
            particle[3] = max(1, particle[3] - 0.05)
            # Create a surface to draw with per-particle alpha
            particle_surf = pygame.Surface((particle[3]*2, particle[3]*2), pygame.SRCALPHA)
            color = (0, 246, 246, max(0, int(particle[4])))
            pygame.draw.circle(particle_surf, color, (int(particle[3]), int(particle[3])), int(particle[3]))
            self.screen.blit(particle_surf, (particle[0], particle[1]))
        # Remove particles that are fully faded
        self.particles = [p for p in self.particles if p[4] > 0]

    def update_text_alpha(self):
        # Increase alpha until fully visible (255)
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + self.fade_in_speed)

    def display_message(self):
        self.update_text_alpha()
        # Render main message with fade-in alpha
        text_surface = self.font.render(self.message, True, self.color)
        text_surface.set_alpha(self.alpha)
        self.screen.blit(
            text_surface,
            (self.screen.get_width() // 2 - text_surface.get_width() // 2,
             self.screen.get_height() // 2 - 150)
        )

        # Render info message with a blinking effect
        blink = (pygame.time.get_ticks() // 500) % 2 == 0
        info_surface = self.font.render(self.info_message, True, (255, 255, 255))
        # Optionally toggle visibility for a blinking effect
        if blink:
            self.screen.blit(
                info_surface,
                (self.screen.get_width() // 2 - info_surface.get_width() // 2,
                 self.screen.get_height() // 2)
            )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.return_to_menu()  # Return to main menu

    def draw(self):
        # Optionally draw a background gradient
        self.draw_background_gradient()
        self.play_music()
        self.add_particles()
        self.update_particles()
        self.display_message()

    def draw_background_gradient(self):
        # Simple vertical gradient for the background
        top_color = (10, 10, 30)
        bottom_color = (40, 40, 80)
        height = self.screen.get_height()
        for y in range(height):
            # Linear interpolation between top and bottom color
            ratio = y / height
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen.get_width(), y))
