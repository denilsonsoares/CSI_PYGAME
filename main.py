#main
import pygame
from scenes.game import Map, Camera
from config.settings import Settings
from entities.Player import Player

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

    # Cria o player
    # Posição x inicial: 400 (centro da tela), Posição y inicial: -32 (fora da tela acima)
    player = Player(400, -32, 32, 32, velocidade=5)

    # Loop do jogo
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(game_settings.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Verifica o estado das teclas
        keys = pygame.key.get_pressed()

        # Movimento para a esquerda
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move_left()
        # Movimento para a direita
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move_right()
        # Nenhuma tecla de movimento pressionada, para o jogador
        else:
            player.stop_moving()

        # Verifica se a tecla de pulo (espaço) foi pressionada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.jump_count < 2:
                player.jump()
        #if keys[pygame.K_SPACE]:
            #player.jump()

        # Atualiza a posição do jogador para simular a queda
        player.loop(game_settings.fps, game_map1)

        # Atualiza a posição da câmera para seguir o jogador
        camera.camera.x = player.rect.centerx - camera.width / 2
        camera.camera.y = player.rect.centery - camera.height / 2

        # Limita a posição da câmera para não sair dos limites do mapa
        camera.camera.x = max(0, min(camera.camera.x, MAP_WIDTH - camera.width))
        camera.camera.y = max(0, min(camera.camera.y, MAP_HEIGHT - camera.height))

        # Desenha o mapa e o fundo deslocados pela câmera
        game_map1.draw(screen, camera)

        # Desenha o jogador
        player.draw(screen, camera.camera.x)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    run_game()
