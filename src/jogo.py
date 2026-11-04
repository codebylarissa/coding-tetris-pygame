import pygame
import sys
import random
from src.constants import FORMATOS_PECAS, fonte, fonte_menu, COR_TEXTO, FPS
from src.tabuleiro import Tabuleiro
from src.telas import executar_pause, executar_game_over, executar_vitoria, executar_vitoria_multiplayer

relogio = pygame.time.Clock()


# ==========================================
# FUNÇÃO DO JOGO (1 JOGADOR)
# ==========================================
def rodar_jogo_1_player(tela):
    try:
        imagem_fundo = pygame.image.load("assets/tetris-bg.png").convert()
        imagem_fundo = pygame.transform.scale(imagem_fundo, (554, 576))
    except FileNotFoundError:
        print("Erro: 'assets/tetris-bg.png' não encontrado!")
        pygame.quit()
        sys.exit()

    try:
        bloco_imagem = pygame.image.load("assets/bloco.png").convert_alpha()
        bloco_imagem = pygame.transform.smoothscale(bloco_imagem, (27, 27))
    except FileNotFoundError:
        print("Erro: 'assets/bloco.png' não foi encontrado na pasta assets!")
        pygame.quit()
        sys.exit()

    canal_linha = None
    som_linha = None
    try:
        som_linha = pygame.mixer.Sound("sounds/line-theme.mp3")
        som_linha.set_volume(0.8)
        canal_linha = pygame.mixer.Channel(1) 
    except Exception as e:
        print(f"Erro ao carregar o som da linha: {e}")

    try:
        pygame.mixer.music.load("sounds/main-theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(0) 
    except Exception as e:
        print(f"Erro ao carregar a música principal: {e}")

    TAMANHO_BLOCO = 27  
    COLUNAS = 10        
    LINHAS = 21        
    OFFSET_X = 42
    OFFSET_Y = 3

    tabuleiro = Tabuleiro(COLUNAS, LINHAS)

    pontuacao = 0
    nivel = 0
    linhas_total = 0

    peca_coluna = 3
    peca_linha = -3
    peca_tipo = random.randint(0, len(FORMATOS_PECAS) - 1)
    peca_rotacao = 0

    proxima_peca_tipo = random.randint(0, len(FORMATOS_PECAS) - 1)
    jogo_perdido = False
    jogo_vencido = False

    def travar_e_limpar():
        nonlocal pontuacao, nivel, linhas_total, jogo_vencido
        linhas_removidas = tabuleiro.limpar_linhas()
        if linhas_removidas > 0:
            pontos_por_linha = [0, 40, 100, 300, 1200]
            pontuacao += pontos_por_linha[linhas_removidas] * (nivel + 1)
            linhas_total += linhas_removidas
            nivel = linhas_total // 10  

            if linhas_total >= 100:
                jogo_vencido = True
                pygame.mixer.music.stop()
            else:
                if canal_linha is not None and som_linha is not None:
                    canal_linha.play(som_linha)

    tempo_ultimo_movimento = pygame.time.get_ticks()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "menu" 
                
            if not jogo_perdido and not jogo_vencido and evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pygame.mixer.music.pause()
                acao_pause = executar_pause(tela)
                if acao_pause == "menu":
                    return "menu"
                else:
                    pygame.mixer.music.unpause()
                    tempo_ultimo_movimento = pygame.time.get_ticks()
                
            if not jogo_perdido and not jogo_vencido and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    if tabuleiro.posicao_valida(peca_coluna - 1, peca_linha, peca_tipo, peca_rotacao):
                        peca_coluna -= 1
                if evento.key == pygame.K_RIGHT:
                    if tabuleiro.posicao_valida(peca_coluna + 1, peca_linha, peca_tipo, peca_rotacao):
                        peca_coluna += 1
                if evento.key == pygame.K_DOWN:
                    if tabuleiro.posicao_valida(peca_coluna, peca_linha + 1, peca_tipo, peca_rotacao):
                        peca_linha += 1
                if evento.key == pygame.K_UP:
                    nova_rotacao = (peca_rotacao + 1) % len(FORMATOS_PECAS[peca_tipo])
                    if tabuleiro.posicao_valida(peca_coluna, peca_linha, peca_tipo, nova_rotacao):
                        peca_rotacao = nova_rotacao

        if not jogo_perdido and not jogo_vencido:
            tempo_atual = pygame.time.get_ticks()
            
            if pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() >= 155000:
                pygame.mixer.music.play(0)
            
            tempo_queda_atual = max(100, 500 - (nivel * 40))
            
            if tempo_atual - tempo_ultimo_movimento > tempo_queda_atual:
                if tabuleiro.posicao_valida(peca_coluna, peca_linha + 1, peca_tipo, peca_rotacao):
                    peca_linha += 1
                else:
                    sucesso = tabuleiro.travar_peca(peca_coluna, peca_linha, peca_tipo, peca_rotacao)
                    if not sucesso:
                        jogo_perdido = True
                        pygame.mixer.music.stop()
                    
                    if not jogo_perdido:
                        travar_e_limpar()
                        
                        teste_proxima_valida = tabuleiro.posicao_valida(3, -3, proxima_peca_tipo, 0)
                        if not teste_proxima_valida:
                            jogo_perdido = True
                        else:
                            peca_tipo = proxima_peca_tipo
                            proxima_peca_tipo = random.randint(0, len(FORMATOS_PECAS) - 1)
                            peca_coluna = 3
                            peca_linha = -3
                            peca_rotacao = 0
                        
                tempo_ultimo_movimento = tempo_atual

        tela.blit(imagem_fundo, (0, 0))

        for lin in range(LINHAS):
            for col in range(COLUNAS):
                if tabuleiro.grid[lin][col] != 0:
                    pos_x = OFFSET_X + (col * TAMANHO_BLOCO)
                    pos_y = OFFSET_Y + (lin * TAMANHO_BLOCO)
                    tela.blit(bloco_imagem, (pos_x, pos_y))

        if not jogo_perdido and not jogo_vencido:
            for col, lin in tabuleiro.obter_posicoes_peca(peca_coluna, peca_linha, peca_tipo, peca_rotacao):
                if lin >= 0:  
                    pos_x_pixels = OFFSET_X + (col * TAMANHO_BLOCO)
                    pos_y_pixels = OFFSET_Y + (lin * TAMANHO_BLOCO)
                    tela.blit(bloco_imagem, (pos_x_pixels, pos_y_pixels))

        texto_pontos = fonte.render(str(pontuacao), True, COR_TEXTO)
        tela.blit(texto_pontos, (550 - texto_pontos.get_width(), 100))

        texto_nivel = fonte.render(str(nivel), True, COR_TEXTO)
        tela.blit(texto_nivel, (525 - texto_nivel.get_width(), 230))

        texto_linhas = fonte.render(str(linhas_total), True, COR_TEXTO)
        tela.blit(texto_linhas, (525 - texto_linhas.get_width(), 330))

        formato_proxima = FORMATOS_PECAS[proxima_peca_tipo][0]
        for bloco in formato_proxima:
            bx = bloco % 4
            by = bloco // 4
            px = 440 + (bx * 20)  
            py = 455 + (by * 20)  
            bloco_pequeno = pygame.transform.smoothscale(bloco_imagem, (20, 20))
            tela.blit(bloco_pequeno, (px, py))

        if jogo_vencido:
            escolha_win = executar_vitoria(tela)
            return escolha_win

        if jogo_perdido:
            escolha_go = executar_game_over(tela)
            return escolha_go

        pygame.display.flip()
        relogio.tick(FPS)


# ==========================================
# FUNÇÃO DO JOGO (2 PLAYERS)
# ==========================================
def rodar_jogo_2_players(tela):
    try:
        bloco_imagem = pygame.image.load("assets/bloco.png").convert_alpha()
        bloco_imagem = pygame.transform.smoothscale(bloco_imagem, (27, 27))
    except FileNotFoundError:
        print("Erro: 'assets/bloco.png' não foi encontrado na pasta assets!")
        pygame.quit()
        sys.exit()

    canal_linha = None
    som_linha = None
    try:
        som_linha = pygame.mixer.Sound("sounds/line-theme.mp3")
        som_linha.set_volume(0.8)
        canal_linha = pygame.mixer.Channel(1) 
    except Exception as e:
        print(f"Erro ao carregar o som da linha: {e}")

    try:
        pygame.mixer.music.load("sounds/main-theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(0) 
    except Exception as e:
        print(f"Erro ao carregar a música principal: {e}")

    try:
        bg_mp = pygame.image.load("assets/tetris-bg.png").convert()
        bg_mp = pygame.transform.scale(bg_mp, (554, 576))
    except Exception as e:
        print(f"Erro ao carregar 'assets/tetris-bg.png': {e}")
        bg_mp = None

    TAMANHO_BLOCO = 27  
    COLUNAS = 10        
    LINHAS = 21        

    OFFSET_X_P1 = 50
    OFFSET_X_P2 = 650
    OFFSET_Y = 35

    tabuleiro_p1 = Tabuleiro(COLUNAS, LINHAS)
    tabuleiro_p2 = Tabuleiro(COLUNAS, LINHAS)

    p1_coluna, p1_linha, p1_tipo, p1_rotacao = 3, -3, random.randint(0, 6), 0
    p1_proxima = random.randint(0, 6)
    p1_pontos, p1_nivel, p1_linhas = 0, 0, 0
    p1_perdido = False

    p2_coluna, p2_linha, p2_tipo, p2_rotacao = 3, -3, random.randint(0, 6), 0
    p2_proxima = random.randint(0, 6)
    p2_pontos, p2_nivel, p2_linhas = 0, 0, 0
    p2_perdido = False

    def processar_linhas_mp(tab, pontuacao, nivel, linhas_total):
        removidas = tab.limpar_linhas()
        if removidas > 0:
            if canal_linha is not None and som_linha is not None:
                canal_linha.play(som_linha)
            pontos_por_linha = [0, 40, 100, 300, 1200]
            pontuacao += pontos_por_linha[removidas] * (nivel + 1)
            linhas_total += removidas
            nivel = linhas_total // 10  
        return pontuacao, nivel, linhas_total

    tempo_ultimo_movimento = pygame.time.get_ticks()

    rodando = True
    while rodando:
        tempo_atual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "menu" 
                
            if evento.type == pygame.KEYDOWN:
                if not p1_perdido:
                    if evento.key == pygame.K_a and tabuleiro_p1.posicao_valida(p1_coluna - 1, p1_linha, p1_tipo, p1_rotacao):
                        p1_coluna -= 1
                    elif evento.key == pygame.K_d and tabuleiro_p1.posicao_valida(p1_coluna + 1, p1_linha, p1_tipo, p1_rotacao):
                        p1_coluna += 1
                    elif evento.key == pygame.K_s and tabuleiro_p1.posicao_valida(p1_coluna, p1_linha + 1, p1_tipo, p1_rotacao):
                        p1_linha += 1
                    elif evento.key == pygame.K_w:
                        nova_rotacao = (p1_rotacao + 1) % len(FORMATOS_PECAS[p1_tipo])
                        if tabuleiro_p1.posicao_valida(p1_coluna, p1_linha, p1_tipo, nova_rotacao):
                            p1_rotacao = nova_rotacao

                if not p2_perdido:
                    if evento.key == pygame.K_LEFT and tabuleiro_p2.posicao_valida(p2_coluna - 1, p2_linha, p2_tipo, p2_rotacao):
                        p2_coluna -= 1
                    elif evento.key == pygame.K_RIGHT and tabuleiro_p2.posicao_valida(p2_coluna + 1, p2_linha, p2_tipo, p2_rotacao):
                        p2_coluna += 1
                    elif evento.key == pygame.K_DOWN and tabuleiro_p2.posicao_valida(p2_coluna, p2_linha + 1, p2_tipo, p2_rotacao):
                        p2_linha += 1
                    elif evento.key == pygame.K_UP:
                        nova_rotacao = (p2_rotacao + 1) % len(FORMATOS_PECAS[p2_tipo])
                        if tabuleiro_p2.posicao_valida(p2_coluna, p2_linha, p2_tipo, nova_rotacao):
                            p2_rotacao = nova_rotacao

        tempo_queda_atual = 400
        if tempo_atual - tempo_ultimo_movimento > tempo_queda_atual:
            if not p1_perdido:
                if tabuleiro_p1.posicao_valida(p1_coluna, p1_linha + 1, p1_tipo, p1_rotacao):
                    p1_linha += 1
                else:
                    sucesso = tabuleiro_p1.travar_peca(p1_coluna, p1_linha, p1_tipo, p1_rotacao)
                    if not sucesso:
                        p1_perdido = True
                    
                    if not p1_perdido:
                        p1_pontos, p1_nivel, p1_linhas = processar_linhas_mp(tabuleiro_p1, p1_pontos, p1_nivel, p1_linhas)
                        p1_tipo = p1_proxima
                        p1_proxima = random.randint(0, 6)
                        p1_coluna, p1_linha, p1_rotacao = 3, -3, 0
                        if not tabuleiro_p1.posicao_valida(p1_coluna, p1_linha, p1_tipo, p1_rotacao):
                            p1_perdido = True

            if not p2_perdido:
                if tabuleiro_p2.posicao_valida(p2_coluna, p2_linha + 1, p2_tipo, p2_rotacao):
                    p2_linha += 1
                else:
                    sucesso = tabuleiro_p2.travar_peca(p2_coluna, p2_linha, p2_tipo, p2_rotacao)
                    if not sucesso:
                        p2_perdido = True
                    
                    if not p2_perdido:
                        p2_pontos, p2_nivel, p2_linhas = processar_linhas_mp(tabuleiro_p2, p2_pontos, p2_nivel, p2_linhas)
                        p2_tipo = p2_proxima
                        p2_proxima = random.randint(0, 6)
                        p2_coluna, p2_linha, p2_rotacao = 3, -3, 0
                        if not tabuleiro_p2.posicao_valida(p2_coluna, p2_linha, p2_tipo, p2_rotacao):
                            p2_perdido = True

            tempo_ultimo_movimento = tempo_atual

        if p1_linhas >= 50:
            pygame.mixer.music.stop()
            escolha_win = executar_vitoria_multiplayer(tela, "JOGADOR 1 VENCEU!")
            return escolha_win
        elif p2_linhas >= 50:
            pygame.mixer.music.stop()
            escolha_win = executar_vitoria_multiplayer(tela, "JOGADOR 2 VENCEU!")
            return escolha_win

        if p1_perdido:
            pygame.mixer.music.stop()
            escolha_win = executar_vitoria_multiplayer(tela, "JOGADOR 2 VENCEU!")
            return escolha_win
        elif p2_perdido:
            pygame.mixer.music.stop()
            escolha_win = executar_vitoria_multiplayer(tela, "JOGADOR 1 VENCEU!")
            return escolha_win

        tela.fill((0, 0, 0))

        if bg_mp:
            tela.blit(bg_mp, (OFFSET_X_P1 - 42, OFFSET_Y))
            tela.blit(bg_mp, (OFFSET_X_P2 - 42, OFFSET_Y))

        txt_p1_titulo = fonte_menu.render("JOGADOR 1", True, (151,184,9))
        txt_p2_titulo = fonte_menu.render("JOGADOR 2", True, (151,184,9))
        tela.blit(txt_p1_titulo, (OFFSET_X_P1 + 45, OFFSET_Y - 30))
        tela.blit(txt_p2_titulo, (OFFSET_X_P2 + 45, OFFSET_Y - 30))

        def desenhar_painel(offset_x, tab, coluna, linha, tipo, rotacao, proxima_tipo, pontos, nivel, linhas):
            for lin in range(LINHAS):
                for col in range(COLUNAS):
                    if tab.grid[lin][col] != 0:
                        px = offset_x + (col * TAMANHO_BLOCO)
                        py = OFFSET_Y + 3 + (lin * TAMANHO_BLOCO)
                        tela.blit(bloco_imagem, (px, py))

            for col, lin in tab.obter_posicoes_peca(coluna, linha, tipo, rotacao):
                if lin >= 0:
                    px = offset_x + (col * TAMANHO_BLOCO)
                    py = OFFSET_Y + 3 + (lin * TAMANHO_BLOCO)
                    tela.blit(bloco_imagem, (px, py))

            base_x = offset_x + 398
            
            txt_p = fonte.render(str(pontos), True, COR_TEXTO)
            tela.blit(txt_p, (base_x + 100 - txt_p.get_width(), OFFSET_Y + 97))

            txt_n = fonte.render(str(nivel), True, COR_TEXTO)
            tela.blit(txt_n, (base_x + 75 - txt_n.get_width(), OFFSET_Y + 227))

            txt_l = fonte.render(str(linhas), True, COR_TEXTO)
            tela.blit(txt_l, (base_x + 75 - txt_l.get_width(), OFFSET_Y + 327))

            formato_prox = FORMATOS_PECAS[proxima_tipo][0]
            for bloco in formato_prox:
                bx = bloco % 4
                by = bloco // 4
                px_p = offset_x + 398 + (bx * 20)
                py_p = OFFSET_Y + 455 + (by * 20)
                bloco_peq = pygame.transform.smoothscale(bloco_imagem, (20, 20))
                tela.blit(bloco_peq, (px_p, py_p))

        desenhar_painel(OFFSET_X_P1, tabuleiro_p1, p1_coluna, p1_linha, p1_tipo, p1_rotacao, p1_proxima, p1_pontos, p1_nivel, p1_linhas)
        desenhar_painel(OFFSET_X_P2, tabuleiro_p2, p2_coluna, p2_linha, p2_tipo, p2_rotacao, p2_proxima, p2_pontos, p2_nivel, p2_linhas)

        pygame.display.flip()
        relogio.tick(FPS)