# main.py
import pygame
import sys
from config import BRANCO, LARGURA_TELA, ALTURA_TELA
from mapa_camera import Mapa
from interacoes import Interacoes

def main():
    # Inicializar Pygame
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption('Quest Mapper')

    # Inicializar o mapa e as interações
    mapa = Mapa()
    interacoes = Interacoes(mapa)

    rodando = True
    clock = pygame.time.Clock()

    while rodando:
        # Lidar com eventos
        rodando = interacoes.lidar_eventos()
        # Desenhar o mapa
        mapa.desenhar(screen, exibir_grid=interacoes.exibir_grid)  
        # Desenhar o menu de seleção de terreno
        interacoes.desenhar_menu(screen)
        # Atualizar a tela
        pygame.display.flip()
        # Controlar a taxa de frames
        clock.tick(60)

    # Encerrar o Pygame
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()