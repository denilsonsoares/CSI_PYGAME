import pygame
from utils.Imports import Imports

class Fire(pygame.sprite.Sprite):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.animation_count = 0
        self.animation_name = "off"
        self.name = "fire"  # Add a name attribute to the Fire object
        self.load_sprites()  # Load sprites after initializing pygame

    def load_sprites(self):
        self.fire_sprites = Imports().load_sprite_sheets("Traps", "Fire", 16, 32)
        self.fire = self.fire_sprites  # Assign fire_sprites to self.fire for easy access

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]  # Access sprites using self.fire
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))
