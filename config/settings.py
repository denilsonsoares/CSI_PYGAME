#settings.py
import pygame

class Settings:
    def __init__(self):
        """Inicializa as configurações do jogo."""
        # Configurações da tela
        self.screen_width = 800
        self.screen_height = 640
        self.bg_color = (230, 230, 230)  # Cor de fundo da tela

        # Configurações de FPS
        self.fps = 60
        # configurações