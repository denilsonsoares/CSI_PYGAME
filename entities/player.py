# player.py
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        # ... (restante da inicialização do jogador)

    def move(self, dx=0, dy=0):
        """Move o jogador por uma certa quantidade (dx, dy)."""
        self.rect.x += dx
        self.rect.y += dy