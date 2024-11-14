# mapa_camera.py
import pygame
import json
from config import *
from tkinter import Tk
from tkinter import filedialog

class Mapa:
    def __init__(self):
        # Criar o mapa como uma matriz 2D de "grama"
        self.mapa = [['grama' for _ in range(MAPA_LARGURA)] for _ in range(MAPA_ALTURA)]
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
        
        # Centralizar a câmera no mapa
        self.centralizar_camera()
        
    def centralizar_camera(self):
        # Calcular as coordenadas do centro do mapa
        centro_x = (MAPA_LARGURA * TAMANHO_TILE) / 2
        centro_y = (MAPA_ALTURA * TAMANHO_TILE) / 2
        
        # Ajustar a posição da câmera para centralizar o mapa
        self.camera_x = centro_x - (LARGURA_TELA / 2)
        self.camera_y = centro_y - (ALTURA_TELA / 2)

    def desenhar(self, screen, exibir_grid=False):
        for linha in range(MAPA_ALTURA):
            for coluna in range(MAPA_LARGURA):
                # Calcular a posição da tile levando em conta a câmera e o zoom
                tile_x = int((coluna * TAMANHO_TILE - self.camera_x) * self.zoom)
                tile_y = int((linha * TAMANHO_TILE - self.camera_y) * self.zoom)
                tile_tamanho = int(TAMANHO_TILE * self.zoom + 1)  # Adiciona uma pequena margem para evitar espaços

                # Desenhar a tile com base no tipo de terreno
                tipo_terreno = self.mapa[linha][coluna]
                cor_tile = TIPOS_TERRENO[tipo_terreno]
                pygame.draw.rect(screen, cor_tile, (tile_x, tile_y, tile_tamanho, tile_tamanho))

                # Desenhar o grid se ativado
                if exibir_grid:
                    pygame.draw.rect(screen, (0, 0, 0), (tile_x, tile_y, tile_tamanho, tile_tamanho), 1)
                
    def mover_camera(self, delta_x, delta_y):
        self.camera_x += delta_x
        self.camera_y += delta_y

        # Limitar a câmera para não sair das bordas
        largura_maxima = (MAPA_LARGURA * TAMANHO_TILE) - (LARGURA_TELA / self.zoom)
        altura_maxima = (MAPA_ALTURA * TAMANHO_TILE) - (ALTURA_TELA / self.zoom)

        self.camera_x = max(0, min(self.camera_x, largura_maxima))
        self.camera_y = max(0, min(self.camera_y, altura_maxima))

    def alterar_terreno(self, mouse_pos, novo_terreno):
        # Traduzir posição do mouse para a posição no mapa
        x_mouse, y_mouse = mouse_pos
        x_tile = int((x_mouse / self.zoom + self.camera_x) // TAMANHO_TILE)
        y_tile = int((y_mouse / self.zoom + self.camera_y) // TAMANHO_TILE)

        # Verificar se a posição está dentro do mapa
        if 0 <= x_tile < MAPA_LARGURA and 0 <= y_tile < MAPA_ALTURA:
            self.mapa[y_tile][x_tile] = novo_terreno

    def ajustar_zoom(self, mouse_pos, delta_zoom):
        mouse_x, mouse_y = mouse_pos
        pos_x_no_mapa = (mouse_x / self.zoom + self.camera_x)
        pos_y_no_mapa = (mouse_y / self.zoom + self.camera_y)

        # Ajustar o zoom com limites
        novo_zoom = self.zoom * delta_zoom
        largura_mapa_visivel = MAPA_LARGURA * TAMANHO_TILE * novo_zoom
        altura_mapa_visivel = MAPA_ALTURA * TAMANHO_TILE * novo_zoom

        if largura_mapa_visivel >= LARGURA_TELA and altura_mapa_visivel >= ALTURA_TELA:
            self.zoom = novo_zoom

        # Recalcular a nova posição
        nova_pos_x_no_mapa = (mouse_x / self.zoom + self.camera_x)
        nova_pos_y_no_mapa = (mouse_y / self.zoom + self.camera_y)

        # Ajustar a câmera para manter o foco no mouse
        self.camera_x += (pos_x_no_mapa - nova_pos_x_no_mapa)
        self.camera_y += (pos_y_no_mapa - nova_pos_y_no_mapa)

        # Limitar a câmera para não sair das bordas
        self.camera_x = max(0, min(self.camera_x, (MAPA_LARGURA * TAMANHO_TILE) - (LARGURA_TELA / self.zoom)))
        self.camera_y = max(0, min(self.camera_y, (MAPA_ALTURA * TAMANHO_TILE) - (ALTURA_TELA / self.zoom)))
        
    def salvar_mapa(self):
        # Inicializa o Tkinter sem criar uma janela principal
        root = Tk()
        root.withdraw()  # Oculta a janela principal do Tkinter

        # Configura o diálogo de salvamento de arquivo
        caminho_arquivo = filedialog.asksaveasfilename(
            defaultextension=".qmp",
            filetypes=[("Arquivos de mapa", "*.qmp"), ("Todos os arquivos", "*.*")],
            title="Salvar mapa como"
        )

        # Verifica se o usuário escolheu um caminho
        if caminho_arquivo:
            # Cria um dicionário com as informações do mapa
            dados_mapa = {
                'largura': MAPA_LARGURA,
                'altura': MAPA_ALTURA,
                'tiles': self.mapa  # Armazena a matriz 2D com os tipos de terreno
            }

            # Salva o dicionário em um arquivo .qmp (pode ser lido como JSON)
            with open(caminho_arquivo, 'w') as arquivo:
                json.dump(dados_mapa, arquivo, indent=4)

            print(f"Mapa salvo em {caminho_arquivo}")
        else:
            print("Operação de salvamento cancelada pelo usuário.")
            
    def importar_mapa(self):
        # Inicializa o Tkinter sem criar uma janela principal
        root = Tk()
        root.withdraw()  # Oculta a janela principal do Tkinter

        # Configura o diálogo de abertura de arquivo
        caminho_arquivo = filedialog.askopenfilename(
            filetypes=[("Arquivos de mapa", "*.qmp"), ("Todos os arquivos", "*.*")],
            title="Importar mapa"
        )

        # Verifica se o usuário escolheu um caminho
        if caminho_arquivo:
            try:
                # Abre o arquivo e carrega os dados como JSON
                with open(caminho_arquivo, 'r') as arquivo:
                    dados_mapa = json.load(arquivo)

                # Verifica se os dados têm a estrutura esperada
                if 'largura' in dados_mapa and 'altura' in dados_mapa and 'tiles' in dados_mapa:
                    self.MAPA_LARGURA = dados_mapa['largura']
                    self.MAPA_ALTURA = dados_mapa['altura']
                    self.mapa = dados_mapa['tiles']  # Carrega a matriz 2D com os tipos de terreno

                    print(f"Mapa importado com sucesso de {caminho_arquivo}")
                else:
                    print("O arquivo importado não contém um formato válido de mapa.")

            except json.JSONDecodeError:
                print("Erro ao decodificar o arquivo. Verifique se ele está em formato JSON válido.")
        else:
            print("Operação de importação cancelada pelo usuário.")