import pygame

class Quadrado:
    def __init__(self, x, y, tamanho, cor, velocidade):
        self.rect = pygame.Rect(x, y, tamanho, tamanho)
        self.velocidade = velocidade  # Velocidade de movimento do quadrado
        self.cor = cor # Cor vermelha
        self.no_chao = True
        self.contador_pulos = 0  # Contador de pulos
        self.velocidade_y = 0  # Velocidade vertical inicial
        self.gravidade = 0.5  # Força da gravidade
        self.forca_pulo = -14  # Força do pulo

    def update(self, mapa):
        # Aplica a gravidade
        if not self.no_chao:
            self.velocidade_y += self.gravidade
            self.rect.y += self.velocidade_y

        # Verifica colisão com o chão
        if mapa.check_collision(self.rect):
            self.rect.y -= self.velocidade_y  # Reverte o último movimento
            self.velocidade_y = 0
            self.no_chao = True
        else:
            self.no_chao = False  # Se não houver colisão, não está no chão

        # Reseta o contador de pulos se estiver no chão
        if self.no_chao:
            self.contador_pulos = 0


    def pulo(self):
    # Se estiver no chão ou se já tiver pulado apenas uma vez, pula
        if self.no_chao or self.contador_pulos < 2:
            self.velocidade_y = self.forca_pulo  # Força do pulo para cima
            self.no_chao = False
            self.contador_pulos += 1

    def draw(self, screen):
        # Desenha o quadrado na tela
        pygame.draw.rect(screen, self.cor, self.rect)


    