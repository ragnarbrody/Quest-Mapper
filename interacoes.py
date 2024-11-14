# interacoes.py
import pygame
from mapa_camera import Mapa
from config import TIPOS_TERRENO, BRANCO

class MenuTerreno:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.opcoes = list(TIPOS_TERRENO.keys())
        self.opcao_selecionada = None

    def desenhar(self, screen):
        # Desenhar a área do menu
        pygame.draw.rect(screen, BRANCO, self.rect)
        font = pygame.font.Font(None, 24)
        
        # Desenhar cada opção
        for i, opcao in enumerate(self.opcoes):
            texto = font.render(opcao.capitalize(), True, (0, 0, 0))
            opcao_rect = pygame.Rect(self.rect.x, self.rect.y + i * 30, self.rect.width, 30)
            pygame.draw.rect(screen, TIPOS_TERRENO[opcao], opcao_rect)
            screen.blit(texto, (opcao_rect.x + 5, opcao_rect.y + 5))
            
            # Verificar seleção com o mouse
            if opcao_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (200, 200, 200), opcao_rect, 2)  # Destacar opção com borda cinza

    def verificar_clique(self, mouse_pos):
        for i, opcao in enumerate(self.opcoes):
            opcao_rect = pygame.Rect(self.rect.x, self.rect.y + i * 30, self.rect.width, 30)
            if opcao_rect.collidepoint(mouse_pos):
                self.opcao_selecionada = opcao
                return opcao
        return None
    
class BotaoHUD:
    def __init__(self, x, y, largura, altura, texto):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.ativo = True  # Estado inicial

    def desenhar(self, screen):
        cor = (200, 200, 200) if self.ativo else (150, 150, 150)
        rect = pygame.draw.rect(screen, cor, self.rect)
        font = pygame.font.Font(None, 24)
        texto = font.render(self.texto, True, (0, 0, 0))
        screen.blit(texto, (self.rect.x + 5, self.rect.y + 5))
        
        if self.ativo == False:
            # Verificar seleção com o mouse
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (200, 200, 200), rect , 2)  # Destacar opção com borda cinza
        else:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (100, 100, 100), rect , 2)  # Destacar opção com borda cinza
            

    def verificar_clique(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.ativo = not self.ativo
            return True
        return False
    
class BotaoHamburguer:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.dropdown_aberto = False  # Indica se o dropdown está visível
        self.opcoes_dropdown = ['Novo Projeto','Salvar', 'Importar', 'Exportar', 'Sair']
        self.selected_option = None
        self.largura_maxima = 0  # Para armazenar a largura do maior texto das opções

    def calcular_largura(self, font):
        # Calcular a largura da maior opção
        self.largura_maxima = max([font.size(opcao)[0] for opcao in self.opcoes_dropdown])
        # Atualizar a largura do botão com base na maior largura
        self.rect.width = self.largura_maxima + 10  # Um pequeno espaço extra para preenchimento

    def desenhar(self, screen):
        cor = (100, 100, 100)
        rect = pygame.draw.rect(screen, cor, self.rect)
        font = pygame.font.Font(None, 24)
        texto = font.render("ESC", True, (255, 255, 255))  # Símbolo de hambúrguer
        screen.blit(texto, (self.rect.x + 5, self.rect.y + 5))
        
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (200, 200, 200), rect , 2)
        
        # Se o dropdown estiver aberto, desenhe as opções
        if self.dropdown_aberto:
            for i, opcao in enumerate(self.opcoes_dropdown):
                opcao_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * 30, self.rect.width, 30)
                pygame.draw.rect(screen, (200, 200, 200), opcao_rect)
                texto_opcao = font.render(opcao, True, (0, 0, 0))
                screen.blit(texto_opcao, (opcao_rect.x + 5, opcao_rect.y + 5))
                if opcao_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (100, 100, 100), opcao_rect , 2)

    def verificar_clique(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.dropdown_aberto = not self.dropdown_aberto
            return True
        # Verificar se alguma opção do dropdown foi clicada
        if self.dropdown_aberto:
            for i, opcao in enumerate(self.opcoes_dropdown):
                opcao_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * 30, self.rect.width, 30)
                if opcao_rect.collidepoint(mouse_pos):
                    self.selected_option = opcao
                    return True
        return False

class Interacoes:
    def __init__(self, mapa):
        self.mapa = mapa
        self.menu_terreno = MenuTerreno(10, 10, 100, 120)
        self.terreno_selecionado = 'cidade'  # Default para adicionar cidades
        self.movendo_camera = False
        self.mouse_posicao_inicial = (0, 0)
        self.botao_grid = BotaoHUD(10, 150, 100, 30, 'Grid On/Off')
        self.botao_hamburguer = BotaoHamburguer(10, 10, 40, 30)  # Botão hambúrguer
        self.exibir_grid = True # Flag para indicar se o grid está visivel
        self.drawing = False  # Flag para indicar se está desenhando

    def lidar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    if self.botao_grid.verificar_clique(pygame.mouse.get_pos()):
                        self.exibir_grid = self.botao_grid.ativo
                    elif self.botao_hamburguer.verificar_clique(pygame.mouse.get_pos()):
                        pass  # O menu hamburguer já alterna a visibilidade do dropdown
                    else:
                        selecionado = self.menu_terreno.verificar_clique(pygame.mouse.get_pos())
                        if selecionado:
                            self.terreno_selecionado = selecionado
                        else:
                            self.mapa.alterar_terreno(pygame.mouse.get_pos(), self.terreno_selecionado)
                            self.drawing = True  # Começar a desenhar
                elif event.button == 3:  # Botão direito para mover a câmera
                    self.movendo_camera = True
                    self.mouse_posicao_inicial = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.movendo_camera = False
                elif event.button == 1:  # Quando o botão esquerdo é solto
                    self.drawing = False  # Parar de desenhar
            elif event.type == pygame.MOUSEMOTION:
                if self.movendo_camera:
                    mouse_pos_atual = pygame.mouse.get_pos()
                    delta_x = self.mouse_posicao_inicial[0] - mouse_pos_atual[0]
                    delta_y = self.mouse_posicao_inicial[1] - mouse_pos_atual[1]
                    self.mapa.mover_camera(delta_x, delta_y)
                    self.mouse_posicao_inicial = mouse_pos_atual
                if self.drawing:  # Desenhar continuamente enquanto o botão esquerdo estiver pressionado
                    self.mapa.alterar_terreno(pygame.mouse.get_pos(), self.terreno_selecionado)
            elif event.type == pygame.MOUSEWHEEL:  # Zoom com a roda do mouse
                if event.y > 0:
                    self.mapa.ajustar_zoom(pygame.mouse.get_pos(), 1.1)
                elif event.y < 0:
                    self.mapa.ajustar_zoom(pygame.mouse.get_pos(), 0.9)

        return True

    def desenhar_menu(self, screen):
        self.menu_terreno.desenhar(screen)
        self.botao_grid.desenhar(screen)
        
        # Calcular a largura máxima das opções do menu hamburguer
        font = pygame.font.Font(None, 24)
        self.botao_hamburguer.calcular_largura(font)
        self.botao_hamburguer.rect.x = screen.get_width() - self.botao_hamburguer.rect.width - 10  # Canto superior direito
        self.botao_hamburguer.desenhar(screen)
        
        if self.botao_hamburguer.selected_option:
            # Exibir ação de acordo com a opção escolhida
            if self.botao_hamburguer.selected_option == 'Salvar':
                self.mapa.salvar_mapa()
                print("Mapa foi salvo!")
            elif self.botao_hamburguer.selected_option == 'Exportar':
                print("Ação: Exportar")
            elif self.botao_hamburguer.selected_option == 'Importar':
                self.mapa.importar_mapa()
                print("Ação: Importar")
            elif self.botao_hamburguer.selected_option == 'Sair':
                print("Ação: Sair")
            elif self.botao_hamburguer.selected_option == 'Novo Projeto':
                print("Ação: Novo Projeto")
            
            # Resetar a seleção após o processamento
            self.botao_hamburguer.selected_option = None