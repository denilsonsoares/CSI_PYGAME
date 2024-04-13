import pygame
import csv

class Camera:
    def __init__(self, mapwidth, mapheight, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.mapwidth = mapwidth
        self.mapheight = mapheight
    
    def update(self):
        # Limita a câmera para não sair dos limites do mapa
        self.camera.clamp_ip(pygame.Rect(0, 0, self.mapwidth, self.mapheight))

class Map:
    def __init__(self, filename):
        self.tiles_data = self.load_map(filename)
        self.tile_images = self.load_tile_images()
        # Inicializa a imagem de fundo como None
        self.background_image = None

    def load_map(self, filename):
        with open(filename, 'r', newline='') as csvfile:
            map_reader = csv.reader(csvfile, delimiter=',')
            map_data = [row for row in map_reader]
        return map_data

    def load_tile_images(self):
        # Carrega a imagem completa que contém todos os tiles
        tileset_image = pygame.image.load('assets/Terrain/terrain_atlas.png')
        tileset_image.convert()
        tile_images = {}

        # Define as coordenadas e o tamanho dos tiles no tileset
        tile_info = {
            '86': {'x': 704, 'y': 256, 'width': 32, 'height': 32},
            # Adicione mais tiles conforme necessário
        }
        # Recorta cada tile e armazena no dicionário
        for tile_number, info in tile_info.items():
            tile_rect = pygame.Rect(info['x'], info['y'], info['width'], info['height'])
            tile_images[tile_number] = tileset_image.subsurface(tile_rect)
        return tile_images
        

    def set_background(self, background_path):
        """Carrega a imagem de fundo."""
        self.background_image = pygame.image.load(background_path)
        self.background_image.convert()
        self.background_rect = self.background_image.get_rect()

    def draw_background(self, screen, camera):
        """Desenha a imagem de fundo ajustada pela câmera."""
        # Calcula a posição da imagem de fundo com base na posição da câmera
        background_position = self.background_rect.move(-camera.camera.x*0.5, -camera.camera.y)
        screen.blit(self.background_image, background_position)

    def draw(self, screen, camera):
        """Desenha a imagem de fundo e os tiles do mapa ajustados pela câmera."""
        # Primeiro desenha a imagem de fundo ajustada pela câmera
        self.draw_background(screen, camera)
        # Depois desenha os tiles do mapa
        for y, row in enumerate(self.tiles_data):
            for x, tile_number in enumerate(row):
                tile_image = self.tile_images.get(tile_number)
                if tile_image:
                    # Ajusta a posição do tile pela posição da câmera
                    tile_rect = tile_image.get_rect()
                    tile_rect.x = x * tile_rect.width - camera.camera.x
                    tile_rect.y = y * tile_rect.height - camera.camera.y
                    screen.blit(tile_image, tile_rect)

    def is_tile_solid(self, x, y):
        """Verifica se o tile na posição (x, y) é sólido."""
        tile_number = self.tiles_data[y][x]
        # Defina quais números de tiles são considerados sólidos
        solid_tiles = ['86']  # Exemplo: '86' é um tile sólido
        return tile_number in solid_tiles

    def check_collision(self, rect):
        """Verifica colisão entre um retângulo e tiles sólidos do mapa."""
        tile_size = 32  # Supondo que cada tile seja 32x32 pixels
        left_tile = rect.left // tile_size
        right_tile = rect.right // tile_size
        top_tile = rect.top // tile_size
        bottom_tile = rect.bottom // tile_size

        # Verifica se algum dos tiles é sólido
        for y in range(top_tile, bottom_tile + 1):
            for x in range(left_tile, right_tile + 1):
                if self.is_tile_solid(x, y):
                    return True  # Há uma colisão
        return False  # Não há colisão
    