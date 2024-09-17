import pygame
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class ScreenFade():
    def __init__(self, direction, colour, speed, fade_type="horizontal", gradient=False, pixelation=False, wave_effect=False):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0
        self.fade_type = fade_type  # 'horizontal', 'vertical', 'radial', 'circular', 'diagonal'
        self.gradient = gradient
        self.pixelation = pixelation
        self.wave_effect = wave_effect
        self.max_fade = SCREEN_WIDTH  # Width of the screen to cover during fade

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed

        # Create a surface with per-pixel alpha support
        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Apply the pixelation effect if enabled
        if self.pixelation:
            self._pixelation_effect(fade_surface)
        # Apply the wave/fisheye effect if enabled
        elif self.wave_effect:
            self._wave_effect(fade_surface)
        # Apply the regular fade based on type if pixelation or wave isn't used
        else:
            if self.fade_type == "horizontal":
                self._fade_horizontal(fade_surface)
            elif self.fade_type == "vertical":
                self._fade_vertical(fade_surface)
            elif self.fade_type == "radial":
                self._fade_radial(fade_surface)
            elif self.fade_type == "circular":
                self._fade_circular(fade_surface)
            elif self.fade_type == "diagonal":
                self._fade_diagonal(fade_surface)

        # Blit the fade surface with transparency onto the screen
        screen.blit(fade_surface, (0, 0))

        # Check if the fade is complete
        if self.fade_counter >= self.max_fade:
            fade_complete = True

        return fade_complete

    def _fade_horizontal(self, surface):
        for i in range(0, SCREEN_WIDTH, self.speed):
            fade_alpha = self._calculate_alpha(self.fade_counter + i)
            fade_color = self._get_fade_color(fade_alpha)
            pygame.draw.rect(surface, fade_color, (i, 0, self.speed, SCREEN_HEIGHT))

    def _fade_vertical(self, surface):
        for i in range(0, SCREEN_HEIGHT, self.speed):
            fade_alpha = self._calculate_alpha(self.fade_counter + i)
            fade_color = self._get_fade_color(fade_alpha)
            pygame.draw.rect(surface, fade_color, (0, i, SCREEN_WIDTH, self.speed))

    def _fade_radial(self, surface):
        for i in range(0, max(SCREEN_WIDTH, SCREEN_HEIGHT), self.speed):
            fade_alpha = self._calculate_alpha(self.fade_counter + i)
            fade_color = self._get_fade_color(fade_alpha)
            pygame.draw.circle(surface, fade_color, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), i)

    def _fade_circular(self, surface):
        radius = int(self.fade_counter * 1.5)
        fade_alpha = self._calculate_alpha(self.fade_counter)
        fade_color = self._get_fade_color(fade_alpha)
        pygame.draw.circle(surface, fade_color, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), radius)

    def _fade_diagonal(self, surface):
        for i in range(0, max(SCREEN_WIDTH, SCREEN_HEIGHT), self.speed):
            fade_alpha = self._calculate_alpha(self.fade_counter + i)
            fade_color = self._get_fade_color(fade_alpha)
            pygame.draw.line(surface, fade_color, (i, 0), (0, i), self.speed)

    def _pixelation_effect(self, surface):
        block_size = max(5, 30 - self.fade_counter // 10)  # Dynamic block size that decreases
        for x in range(0, SCREEN_WIDTH, block_size):
            for y in range(0, SCREEN_HEIGHT, block_size):
                fade_alpha = self._calculate_alpha(self.fade_counter)
                fade_color = self._get_fade_color(fade_alpha)
                pygame.draw.rect(surface, fade_color, (x, y, block_size, block_size))

    def _wave_effect(self, surface):
        wave_amplitude = 30  # Customize this value for effect size
        for i in range(0, SCREEN_WIDTH, self.speed):
            fade_alpha = self._calculate_alpha(self.fade_counter + i)
            fade_color = self._get_fade_color(fade_alpha)
            offset_y = int(wave_amplitude * math.sin(self.fade_counter / 20 + i / 50))  # Wave effect calculation
            pygame.draw.rect(surface, fade_color, (i, SCREEN_HEIGHT // 2 + offset_y, self.speed, SCREEN_HEIGHT))

    def _get_fade_color(self, alpha):
        """Helper function to return RGBA color."""
        return (self.colour[0], self.colour[1], self.colour[2], alpha)

    def _calculate_alpha(self, value):
        """Calculate alpha value to fade from dark to transparent."""
        return max(0, min(255, 255 - int(value * 255 / self.max_fade)))

