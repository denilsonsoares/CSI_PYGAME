# main.py
import pygame
from scenes.game import Map, Camera
from config.settings import Settings
from scenes.teste import Quadrado
from entities.player import Player
from entities.enemy import Enemy
from os import listdir
from os.path import isfile, join

def run_game():

    pygame.init()
    pygame.display.set_caption("FUND")
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))

    # Configurações do mapa
    MAP_WIDTH, MAP_HEIGHT = 12800, 640
    game_map1 = Map('scenes/mapa1.csv')  # Substitua pelo caminho correto do arquivo CSV
    game_map1.set_background('assets/Background/backgroundF1.png')

    # Cria a câmera
    camera = Camera(MAP_WIDTH, MAP_HEIGHT, game_settings.screen_width, game_settings.screen_height)

    # Cria um quadrado vermelho de 5x5 pixels
    tamanho_do_quadrado = 10
    cor = (255,0,0)
    quadrado_velocidade=10
    quadrado_vermelho = Quadrado(400,600,tamanho_do_quadrado, cor, quadrado_velocidade)
    tecla_espaco_pressionada =False

    #looping do jogo
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(game_settings.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run =False
            # Verifica se a barra de espaço foi pressionada para pular
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Verifica se a tecla espaço foi recém-pressionada
                    if not tecla_espaco_pressionada:
                        quadrado_vermelho.pulo()
                        tecla_espaco_pressionada = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # Reseta o estado da tecla espaço quando ela é liberada
                    tecla_espaco_pressionada = False
        # Obtém as teclas pressionadas
        keys = pygame.key.get_pressed()
        # Atualiza os deslocamentos com base nas teclas pressionadas
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            camera.camera.x -= quadrado_vermelho.velocidade
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            camera.camera.x += quadrado_vermelho.velocidade

        quadrado_vermelho.update(game_map1) #atualiza o quadrado
        game_map1.draw(screen, camera)  # Desenha o mapa e o fundo deslocados pela camera
        quadrado_vermelho.draw(screen)  # Desenha o quadrado
        camera.update()#atualiza a camera para o mapa nao sair da tela
        pygame.display.flip()
    pygame.quit()

if __name__ =='__main__': 
    run_game()
