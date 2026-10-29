import pygame
import sys
import random

# Inicialização do som e do pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

pygame.mixer.set_num_channels(8)

# Definições da tela
LARGURA_TELA = 554
ALTURA_TELA = 576
FPS = 60

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Tetris")

relogio = pygame.time.Clock()

# Carregamento da fonte
try:
    fonte = pygame.font.Font("fonts/Early Gameboy.ttf", 26)
except Exception as e:
    print(f"Erro ao carregar a fonte, usando padrão: {e}")
    fonte = pygame.font.Font(None, 24)

COR_TEXTO = (0, 48, 0)

# Execução da música principal em loop 
try:
    pygame.mixer.music.load("sounds/main-theme.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(0) 
except Exception as e:
    print(f"Erro ao carregar a música principal: {e}")

# Carregamento do som da linha
canal_linha = None
som_linha = None
try:
    som_linha = pygame.mixer.Sound("sounds/line-theme.mp3")
    som_linha.set_volume(0.8)
    canal_linha = pygame.mixer.Channel(1) 
except Exception as e:
    print(f"Erro ao carregar o som da linha: {e}")

# Carregamento do cenário
try:
    imagem_fundo = pygame.image.load("assets/tetris-bg.png").convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA_TELA, ALTURA_TELA))
except FileNotFoundError:
    print("Erro: 'assets/tetris-bg.png' não encontrado!")
    pygame.quit()
    sys.exit()

# Construção do grid 
TAMANHO_BLOCO = 27  
COLUNAS = 10        
LINHAS = 21         

OFFSET_X = 42
OFFSET_Y = 3

# Carregamento do tetramino
try:
    bloco_imagem = pygame.image.load("assets/bloco.png").convert_alpha()
    bloco_imagem = pygame.transform.smoothscale(bloco_imagem, (TAMANHO_BLOCO, TAMANHO_BLOCO))
except FileNotFoundError:
    print("Erro: 'assets/bloco.png' não foi encontrado na pasta assets!")
    pygame.quit()
    sys.exit()

# Matriz do grid
grid = [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]

# Formatos das peças
FORMATOS_PECAS = [
    [[1, 5, 9, 13], [4, 5, 6, 7]], # I
    [[4, 5, 9, 10], [2, 6, 5, 9]], # Z
    [[6, 7, 5, 9], [1, 5, 6, 10]], # S
    [[1, 5, 9, 10], [0, 4, 5, 6], [1, 2, 6, 10], [4, 5, 6, 2]], # L
    [[1, 5, 9, 8], [0, 1, 5, 9], [1, 5, 9, 2], [4, 5, 6, 10]], # J
    [[4, 5, 6, 9], [1, 5, 9, 6], [4, 5, 6, 1], [1, 5, 9, 4]], # T
    [[1, 2, 5, 6]] # Quadrado
]

# Variáveis de pontuação 
pontuacao = 0
nivel = 0
linhas_total = 0

# Variáveis para controlar a peça atual e a próxima peça
peca_coluna = 3
peca_linha = -3
peca_tipo = random.randint(0, len(FORMATOS_PECAS) - 1)
peca_rotacao = 0

proxima_peca_tipo = random.randint(0, len(FORMATOS_PECAS) - 1)

# Estado de game over
jogo_perdido = False

# Função para calcular as posições dos blocos da peça
def obter_posicoes_peca(coluna, linha, tipo, rotacao):
    formato = FORMATOS_PECAS[tipo][rotacao]
    posicoes = []
    for bloco in formato:
        deslocamento_x = bloco % 4
        deslocamento_y = bloco // 4
        posicoes.append((coluna + deslocamento_x, linha + deslocamento_y))
    return posicoes

# Função para verificar se a posição é válida
def posicao_valida(coluna, linha, tipo, rotacao):
    for col, lin in obter_posicoes_peca(coluna, linha, tipo, rotacao):
        if col < 0 or col >= COLUNAS or lin >= LINHAS:
            return False
        if lin >= 0 and grid[lin][col] != 0:
            return False
    return True

# Função para limpar linhas completas, contar pontos e tocar o som
def limpar_linhas_e_tocar_som():
    global grid, pontuacao, nivel, linhas_total
    novas_linhas = [linha for linha in grid if any(celula == 0 for celula in linha)]
    linhas_removidas = LINHAS - len(novas_linhas)
    
    if linhas_removidas > 0:
        if canal_linha is not None and som_linha is not None:
            canal_linha.play(som_linha)
            
        pontos_por_linha = [0, 40, 100, 300, 1200]
        pontuacao += pontos_por_linha[linhas_removidas] * (nivel + 1)
        linhas_total += linhas_removidas
        nivel = linhas_total // 10  
            
        linhas_vazias = [[0 for _ in range(COLUNAS)] for _ in range(linhas_removidas)]
        grid = linhas_vazias + novas_linhas

# Função para fixar a peça atual no grid
def travar_peca():
    global grid, pontuacao, nivel, linhas_total, jogo_perdido
    for col, lin in obter_posicoes_peca(peca_coluna, peca_linha, peca_tipo, peca_rotacao):
        if lin >= 0:
            grid[lin][col] = 1
        else:
            # Se uma peça travou e parte dela ficou acima da linha 0 o jogo para
            jogo_perdido = True
            pygame.mixer.music.stop()
            
    if not jogo_perdido:
        limpar_linhas_e_tocar_som()

# Controle de tempo para a queda automática
TEMPO_QUEDA = 500 
tempo_ultimo_movimento = pygame.time.get_ticks()

# Loop principal
rodando = True
while rodando:

    # Captura de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
        if not jogo_perdido and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                if posicao_valida(peca_coluna - 1, peca_linha, peca_tipo, peca_rotacao):
                    peca_coluna -= 1
                    
            if evento.key == pygame.K_RIGHT:
                if posicao_valida(peca_coluna + 1, peca_linha, peca_tipo, peca_rotacao):
                    peca_coluna += 1
                
            if evento.key == pygame.K_DOWN:
                if posicao_valida(peca_coluna, peca_linha + 1, peca_tipo, peca_rotacao):
                    peca_linha += 1
                
            if evento.key == pygame.K_UP:
                nova_rotacao = (peca_rotacao + 1) % len(FORMATOS_PECAS[peca_tipo])
                valido = True
                for col, lin in obter_posicoes_peca(peca_coluna, peca_linha, peca_tipo, nova_rotacao):
                    if col < 0 or col >= COLUNAS or lin >= LINHAS:
                        valido = False
                        break
                    if lin >= 0 and grid[lin][col] != 0:
                        valido = False
                        break
                if valido:
                    peca_rotacao = nova_rotacao

    # Queda das peças 
    if not jogo_perdido:
        tempo_atual = pygame.time.get_ticks()
        
        # Reinicia a música principal se chegar em 02:35
        if pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() >= 155000:
            pygame.mixer.music.play(0)
        
        # Velocidade de queda aumenta conforme o nível sobe
        tempo_queda_atual = max(100, 500 - (nivel * 40)) 
        
        if tempo_atual - tempo_ultimo_movimento > tempo_queda_atual:
            if posicao_valida(peca_coluna, peca_linha + 1, peca_tipo, peca_rotacao):
                peca_linha += 1
            else:
                travar_peca()
                
                # Verifica se a próxima peça já nasce batendo no topo
                teste_proxima_valida = posicao_valida(3, -3, proxima_peca_tipo, 0)
                
                if not teste_proxima_valida:
                    jogo_perdido = True
                    pygame.mixer.music.stop()
                else:
                    # Se não, ela desce para o grid
                    peca_tipo = proxima_peca_tipo
                    proxima_peca_tipo = random.randint(0, len(FORMATOS_PECAS) - 1)
                    
                    peca_coluna = 3
                    peca_linha = -3
                    peca_rotacao = 0
                    
            tempo_ultimo_movimento = tempo_atual

    # Desenha o fundo na tela
    tela.blit(imagem_fundo, (0, 0))

    # Desenha todos os blocos salvos no grid
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if grid[lin][col] != 0:
                pos_x = OFFSET_X + (col * TAMANHO_BLOCO)
                pos_y = OFFSET_Y + (lin * TAMANHO_BLOCO)
                tela.blit(bloco_imagem, (pos_x, pos_y))

    # Desenha a peça que está caindo 
    if not jogo_perdido:
        for col, lin in obter_posicoes_peca(peca_coluna, peca_linha, peca_tipo, peca_rotacao):
            if lin >= 0:  
                pos_x_pixels = OFFSET_X + (col * TAMANHO_BLOCO)
                pos_y_pixels = OFFSET_Y + (lin * TAMANHO_BLOCO)
                tela.blit(bloco_imagem, (pos_x_pixels, pos_y_pixels))

    # Score
    texto_pontos = fonte.render(str(pontuacao), True, COR_TEXTO)
    tela.blit(texto_pontos, (550 - texto_pontos.get_width(), 100))

    # Level
    texto_nivel = fonte.render(str(nivel), True, COR_TEXTO)
    tela.blit(texto_nivel, (525 - texto_nivel.get_width(), 230))

    # Lines
    texto_linhas = fonte.render(str(linhas_total), True, COR_TEXTO)
    tela.blit(texto_linhas, (525 - texto_linhas.get_width(), 330))

    # Próxima peça
    formato_proxima = FORMATOS_PECAS[proxima_peca_tipo][0]
    for bloco in formato_proxima:
        bx = bloco % 4
        by = bloco // 4
        
        px = 440 + (bx * 20)  
        py = 455 + (by * 20)  
        
        bloco_pequeno = pygame.transform.smoothscale(bloco_imagem, (20, 20))
        tela.blit(bloco_pequeno, (px, py))

    # Atualiza o display
    pygame.display.flip()

    relogio.tick(FPS)

pygame.quit()
sys.exit()