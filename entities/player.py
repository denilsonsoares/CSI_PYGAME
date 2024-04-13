import pygame
from utils.Imports import Imports

class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    ANIMATION_DELAY = 2

    def __init__(self, x, y, width, height, velocidade=5):  # Adicione o atributo velocidade
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.velocidade = velocidade  # Atributo de velocidade para mover o player
        self.load_sprites()  # Load sprites after initializing pygame

    def load_sprites(self):
        self.SPRITES = Imports().load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    def move_left(self):
        self.x_vel = -self.velocidade
        self.direction = "left"
        self.update_sprite()

    def move_right(self):
        self.x_vel = self.velocidade
        self.direction = "right"
        self.update_sprite()

    def stop_moving(self):
        self.x_vel = 0

    def jump(self):
        if self.jump_count < 2:  # Permitir apenas dois pulos (0 e 1)
            if self.jump_count == 0 or self.fall_count == 0:  # Permitir pulo apenas no chão ou no primeiro pulo
                self.y_vel = -self.GRAVITY * 8
                self.animation_count = 0
                self.jump_count += 1
                if self.jump_count == 1:
                    self.fall_count = 0

    def loop(self, fps, game_map):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        # Verificar colisão com o chão
        self.check_collision_with_ground(game_map)

        if self.jump_count > 0 and self.fall_count > 0:
            self.jump_count = 2  # Impede novos pulos até tocar o chão

        if self.hit:
            self.hit_count += 1
            if self.hit_count > fps * 2:
                self.hit = False
                self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()
    def check_collision_with_ground(self, game_map):
        # Calcula a futura posição do jogador
        future_rect = self.rect.copy()
        future_rect.y += self.y_vel  # Aplica a velocidade vertical

        # Verifica se há colisão com o chão (tiles sólidos)
        if game_map.check_collision(future_rect):
            # Se houver colisão, ajusta a posição vertical para ficar no topo do chão
            tile_size = 32  # Tamanho do tile (32x32 pixels, conforme definido)
            tile_y = future_rect.bottom // tile_size  # Obtém a linha do tile abaixo do jogador
            landing_y = tile_y * tile_size  # Calcula a posição no topo do chão

            # Atualiza a posição vertical do jogador para ficar no topo do chão
            self.rect.bottom = landing_y
            self.landed()  # Marca que o jogador aterrissou no chão
            self.y_vel = 0  # Reseta a velocidade vertical
            self.jump_count = 0  # Permite outro pulo após tocar no chão

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
