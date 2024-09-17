import pygame

BG = (0, 0, 0)

class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the image with alpha channel to preserve transparency
        self.image = pygame.image.load('assets/images/traps/on.png').convert_alpha()
        
        self.frame_width = self.image.get_width() // 3
        self.frame_height = self.image.get_height()
        self.frames = []
        
        for i in range(3):
            frame_rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame_image = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame_image.blit(self.image, (0, 0), frame_rect)
            self.frames.append(frame_image)
        
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_speed = 0.1  # Adjust the animation speed as needed

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
