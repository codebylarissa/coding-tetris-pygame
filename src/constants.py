import pygame

# Inicialização rápida de fontes para uso global
pygame.font.init()

try:
    fonte = pygame.font.Font("fonts/Early Gameboy.ttf", 26)
    fonte_menu = pygame.font.Font("fonts/Early Gameboy.ttf", 20)
    fonte_pequena = pygame.font.Font("fonts/Early Gameboy.ttf", 14)
except Exception as e:
    print(f"Erro ao carregar a fonte, usando padrão: {e}")
    fonte = pygame.font.Font(None, 24)
    fonte_menu = pygame.font.Font(None, 20)
    fonte_pequena = pygame.font.Font(None, 18)

# Definições de resoluções
LARGURA_PADRAO, ALTURA_PADRAO = 554, 576
LARGURA_MP, ALTURA_MP = 1200, 620
FPS = 60

COR_TEXTO = (0, 48, 0)
COR_BG_CAIXA = (155, 188, 15)

# Formatos das peças do Tetris
FORMATOS_PECAS = [
    [[1, 5, 9, 13], [4, 5, 6, 7]], # I
    [[4, 5, 9, 10], [2, 6, 5, 9]], # Z
    [[6, 7, 5, 9], [1, 5, 6, 10]], # S
    [[1, 5, 9, 10], [0, 4, 5, 6], [1, 2, 6, 10], [4, 5, 6, 2]], # L
    [[1, 5, 9, 8], [0, 1, 5, 9], [1, 5, 9, 2], [4, 5, 6, 10]], # J
    [[4, 5, 6, 9], [1, 5, 9, 6], [4, 5, 6, 1], [1, 5, 9, 4]], # T
    [[1, 2, 5, 6]] # Quadrado
]