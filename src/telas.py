import pygame
import sys
from src.constants import fonte, fonte_menu, fonte_pequena, COR_TEXTO, LARGURA_PADRAO, ALTURA_PADRAO, LARGURA_MP, ALTURA_MP, FPS

relogio = pygame.time.Clock()

def executar_menu(tela):
    selected_option = 1  
    
    try:
        menu_bg = pygame.image.load("assets/menu-bg.png").convert()
        menu_bg = pygame.transform.scale(menu_bg, (LARGURA_PADRAO, ALTURA_PADRAO))
    except Exception as e:
        print(f"Erro ao carregar 'assets/menu-bg.png': {e}")
        menu_bg = None

    try:
        pygame.mixer.music.load("sounds/menu-theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1) 
    except Exception as e:
        print(f"Erro ao carregar 'sounds/menu-theme.mp3': {e}")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    selected_option = 2 if selected_option == 1 else 1
                elif evento.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    return selected_option

        tela.fill((0, 0, 0))
        if menu_bg:
            tela.blit(menu_bg, (0, 0))
        
        if menu_bg:
            cor_fundo_caixa = menu_bg.get_at((310, 520))
            pygame.draw.rect(tela, cor_fundo_caixa, (290, 500, 210, 35))

        text_1p = "1 PLAYER"
        text_2p = "2 PLAYER"
        
        p1_x, p1_y = 65, 495
        p2_x, p2_y = 315, 495

        render_1p = fonte_menu.render(text_1p, True, COR_TEXTO)
        render_2p = fonte_menu.render(text_2p, True, COR_TEXTO)

        tela.blit(render_1p, (p1_x, p1_y))
        tela.blit(render_2p, (p2_x, p2_y))

        if selected_option == 1:
            seta_x = p1_x - 15
            seta_y = p1_y + 4
        else:
            seta_x = p2_x - 15
            seta_y = p2_y + 4

        pontos_triangulo = [
            (seta_x, seta_y),       
            (seta_x, seta_y + 12),  
            (seta_x + 8, seta_y + 6) 
        ]
        pygame.draw.polygon(tela, COR_TEXTO, pontos_triangulo)

        pygame.display.flip()
        relogio.tick(FPS)


def executar_pause(tela):
    selected_option = 1  
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    selected_option = 2 if selected_option == 1 else 1
                elif evento.key == pygame.K_RETURN:
                    if selected_option == 1:
                        return "continuar"
                    else:
                        return "menu"
                elif evento.key == pygame.K_SPACE:
                    return "continuar"

        largura_caixa = 270
        altura_caixa = 220
        pos_x = 42
        pos_y = (ALTURA_PADRAO - altura_caixa) // 2

        pygame.draw.rect(tela, (151, 184, 9), (pos_x, pos_y, largura_caixa, altura_caixa))
        pygame.draw.rect(tela, (56, 98, 17), (pos_x, pos_y, largura_caixa, altura_caixa), 4)

        txt_titulo = fonte_menu.render("PAUSE", True, COR_TEXTO)
        render_cont = fonte_pequena.render("CONTINUAR", True, COR_TEXTO)
        render_menu = fonte_pequena.render("VOLTAR AO MENU", True, COR_TEXTO)

        tela.blit(txt_titulo, (pos_x + (largura_caixa // 2 - txt_titulo.get_width() // 2), pos_y + 35))
        
        c_x, c_y = pos_x + 40, pos_y + 100
        m_x, m_y = pos_x + 40, pos_y + 145

        tela.blit(render_cont, (c_x, c_y))
        tela.blit(render_menu, (m_x, m_y))

        if selected_option == 1:
            seta_x = c_x - 18
            seta_y = c_y + 1
        else:
            seta_x = m_x - 18
            seta_y = m_y + 1

        pontos_triangulo = [
            (seta_x, seta_y),       
            (seta_x, seta_y + 10),  
            (seta_x + 7, seta_y + 5) 
        ]
        pygame.draw.polygon(tela, COR_TEXTO, pontos_triangulo)

        pygame.display.flip()
        relogio.tick(FPS)


def executar_game_over(tela):
    selected_option = 1  
    
    try:
        pygame.mixer.music.load("sounds/game-over-theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(0) 
    except Exception as e:
        print(f"Erro ao carregar a música de game over: {e}")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    selected_option = 2 if selected_option == 1 else 1
                elif evento.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    if selected_option == 1:
                        return "reiniciar"
                    else:
                        return "menu"

        largura_caixa = 270
        altura_caixa = 220
        pos_x = 42
        pos_y = (ALTURA_PADRAO - altura_caixa) // 2

        pygame.draw.rect(tela, (151, 184, 9), (pos_x, pos_y, largura_caixa, altura_caixa))
        pygame.draw.rect(tela, (56, 98, 17), (pos_x, pos_y, largura_caixa, altura_caixa), 4)

        txt_titulo = fonte_menu.render("GAME OVER", True, COR_TEXTO)
        render_novamente = fonte_pequena.render("JOGAR DE NOVO", True, COR_TEXTO)
        render_menu = fonte_pequena.render("VOLTAR AO MENU", True, COR_TEXTO)

        tela.blit(txt_titulo, (pos_x + (largura_caixa // 2 - txt_titulo.get_width() // 2), pos_y + 35))
        
        n_x, n_y = pos_x + 30, pos_y + 100
        m_x, m_y = pos_x + 30, pos_y + 145

        tela.blit(render_novamente, (n_x, n_y))
        tela.blit(render_menu, (m_x, m_y))

        if selected_option == 1:
            seta_x = n_x - 18
            seta_y = n_y + 1
        else:
            seta_x = m_x - 18
            seta_y = m_y + 1

        pontos_triangulo = [
            (seta_x, seta_y),       
            (seta_x, seta_y + 10),  
            (seta_x + 7, seta_y + 5) 
        ]
        pygame.draw.polygon(tela, COR_TEXTO, pontos_triangulo)

        pygame.display.flip()
        relogio.tick(FPS)


def executar_vitoria(tela):
    selected_option = 1  
    
    try:
        pygame.mixer.music.load("sounds/win-theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(0) 
    except Exception as e:
        print(f"Erro ao carregar a música de vitória: {e}")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    selected_option = 2 if selected_option == 1 else 1
                elif evento.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    if selected_option == 1:
                        return "reiniciar"
                    else:
                        return "menu"

        largura_caixa = 270
        altura_caixa = 220
        pos_x = 42
        pos_y = (ALTURA_PADRAO - altura_caixa) // 2

        pygame.draw.rect(tela, (151, 184, 9), (pos_x, pos_y, largura_caixa, altura_caixa))
        pygame.draw.rect(tela, (56, 98, 17), (pos_x, pos_y, largura_caixa, altura_caixa), 4)

        txt_titulo = fonte_menu.render("VOCE VENCEU!", True, COR_TEXTO)
        render_novamente = fonte_pequena.render("JOGAR DE NOVO", True, COR_TEXTO)
        render_menu = fonte_pequena.render("VOLTAR AO MENU", True, COR_TEXTO)

        tela.blit(txt_titulo, (pos_x + (largura_caixa // 2 - txt_titulo.get_width() // 2), pos_y + 35))
        
        n_x, n_y = pos_x + 30, pos_y + 100
        m_x, m_y = pos_x + 30, pos_y + 145

        tela.blit(render_novamente, (n_x, n_y))
        tela.blit(render_menu, (m_x, m_y))

        if selected_option == 1:
            seta_x = n_x - 18
            seta_y = n_y + 1
        else:
            seta_x = m_x - 18
            seta_y = m_y + 1

        pontos_triangulo = [
            (seta_x, seta_y),       
            (seta_x, seta_y + 10),  
            (seta_x + 7, seta_y + 5) 
        ]
        pygame.draw.polygon(tela, COR_TEXTO, pontos_triangulo)

        pygame.display.flip()
        relogio.tick(FPS)


def executar_vitoria_multiplayer(tela, vencedor_texto):
    selected_option = 1  
    
    try:
        pygame.mixer.music.load("sounds/win-theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(0) 
    except Exception as e:
        print(f"Erro ao carregar a música de vitória: {e}")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    selected_option = 2 if selected_option == 1 else 1
                elif evento.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    if selected_option == 1:
                        return "reiniciar"
                    else:
                        return "menu"

        largura_caixa = 460
        altura_caixa = 260
        pos_x = (LARGURA_MP - largura_caixa) // 2
        pos_y = (ALTURA_MP - altura_caixa) // 2

        pygame.draw.rect(tela, (151, 184, 9), (pos_x, pos_y, largura_caixa, altura_caixa))
        pygame.draw.rect(tela, (56, 98, 17), (pos_x, pos_y, largura_caixa, altura_caixa), 4)

        txt_titulo = fonte.render(vencedor_texto, True, COR_TEXTO)
        render_novamente = fonte_menu.render("JOGAR DE NOVO", True, COR_TEXTO)
        render_menu = fonte_menu.render("VOLTAR AO MENU", True, COR_TEXTO)

        tela.blit(txt_titulo, (pos_x + (largura_caixa // 2 - txt_titulo.get_width() // 2), pos_y + 40))
        
        n_x, n_y = pos_x + 60, pos_y + 120
        m_x, m_y = pos_x + 60, pos_y + 180

        tela.blit(render_novamente, (n_x, n_y))
        tela.blit(render_menu, (m_x, m_y))

        if selected_option == 1:
            seta_x = n_x - 25
            seta_y = n_y + 4
        else:
            seta_x = m_x - 25
            seta_y = m_y + 4 

        pontos_triangulo = [
            (seta_x, seta_y),       
            (seta_x, seta_y + 14),  
            (seta_x + 10, seta_y + 7) 
        ]
        pygame.draw.polygon(tela, COR_TEXTO, pontos_triangulo)

        pygame.display.flip()
        relogio.tick(FPS)

def executar_instrucoes_solo(tela):
    try:
        imagem_fundo = pygame.image.load("assets/tetris-bg.png").convert()
        imagem_fundo = pygame.transform.scale(imagem_fundo, (tela.get_width(), tela.get_height()))
    except Exception:
        imagem_fundo = None

    try:
        pygame.mixer.music.load("sounds/main-theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Erro ao carregar a música: {e}")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return "jogar"
                elif evento.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return "menu"

        tela.fill((0, 0, 0))
        if imagem_fundo:
            tela.blit(imagem_fundo, (0, 0))

        # Caixa no tamanho padrão ideal (igual à de vitória)
        largura_caixa = 460
        altura_caixa = 340
        pos_x = (tela.get_width() - largura_caixa) // 2
        pos_y = (tela.get_height() - altura_caixa) // 2

        pygame.draw.rect(tela, (151, 184, 9), (pos_x, pos_y, largura_caixa, altura_caixa))
        pygame.draw.rect(tela, (56, 98, 17), (pos_x, pos_y, largura_caixa, altura_caixa), 4)

        txt_titulo = fonte_menu.render("COMO JOGAR", True, COR_TEXTO)
        tela.blit(txt_titulo, (pos_x + (largura_caixa // 2 - txt_titulo.get_width() // 2), pos_y + 20))

        # Usando a 'fonte' padrão (mesmo tamanho da tela de vitória)
        regras = [
            "SETA ESQ E DIR - MOVE A PECA",
            "SETA DE BAIXO - ACELERA A QUEDA",
            "SETA DE CIMA - ROTACIONA A PECA",
            "ESPACO - PAUSA O JOGO",
            "OBJETIVO - FACA 100 LINHAS",
            "PARA VENCER",
            "",
            "PRESSIONE ENTER PARA COMECAR"
        ]

        espaco_y = pos_y + 75
        for linha in regras:
            txt_linha = fonte_pequena.render(linha, True, COR_TEXTO)
            tela.blit(txt_linha, (pos_x + (largura_caixa - txt_linha.get_width()) // 2, espaco_y))
            espaco_y += 34

        pygame.display.flip()
        relogio.tick(FPS)


def executar_instrucoes_multi(tela):
    try:
        bg_mp = pygame.image.load("assets/tetris-bg.png").convert()
        bg_mp = pygame.transform.scale(bg_mp, (554, 576))
    except Exception:
        bg_mp = None

    try:
        pygame.mixer.music.load("sounds/main-theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Erro ao carregar a música: {e}")

    OFFSET_X_P1 = 50
    OFFSET_X_P2 = 650
    OFFSET_Y = 35

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return "jogar"
                elif evento.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return "menu"

        # Desenha o cenário de fundo real do multiplayer (idêntico ao jogo e à tela de vitória)
        tela.fill((0, 0, 0))

        if bg_mp:
            tela.blit(bg_mp, (OFFSET_X_P1 - 42, OFFSET_Y))
            tela.blit(bg_mp, (OFFSET_X_P2 - 42, OFFSET_Y))

        txt_p1_titulo = fonte_menu.render("JOGADOR 1", True, (151, 184, 9))
        txt_p2_titulo = fonte_menu.render("JOGADOR 2", True, (151, 184, 9))
        tela.blit(txt_p1_titulo, (OFFSET_X_P1 + 45, OFFSET_Y - 30))
        tela.blit(txt_p2_titulo, (OFFSET_X_P2 + 45, OFFSET_Y - 30))

        # Desenha a caixa de instruções por cima do cenário do jogo
        largura_caixa = 560
        altura_caixa = 420
        pos_x = (tela.get_width() - largura_caixa) // 2
        pos_y = (tela.get_height() - altura_caixa) // 2

        pygame.draw.rect(tela, (151, 184, 9), (pos_x, pos_y, largura_caixa, altura_caixa))
        pygame.draw.rect(tela, (56, 98, 17), (pos_x, pos_y, largura_caixa, altura_caixa), 4)

        txt_titulo = fonte_menu.render("COMO JOGAR", True, COR_TEXTO)
        tela.blit(txt_titulo, (pos_x + (largura_caixa // 2 - txt_titulo.get_width() // 2), pos_y + 20))

        regras = [
            "JOGADOR 1:",
            "TECLAS A E D - MOVE A PECA",
            "TECLA S - ACELERA A QUEDA",
            "TECLA W - ROTACIONA A PECA",
            "JOGADOR 2:",
            "SETA ESQ E DIR - MOVE A PECA",
            "SETA DE BAIXO - ACELERA A QUEDA",
            "SETA DE CIMA - ROTACIONA A PECA",
            "OBJETIVO - FACA 50 LINHAS PARA VENCER",
            "",
            "PRESSIONE ENTER PARA COMECAR"
        ]

        espaco_y = pos_y + 70
        for linha in regras:
            txt_linha = fonte_pequena.render(linha, True, COR_TEXTO)
            tela.blit(txt_linha, (pos_x + (largura_caixa - txt_linha.get_width()) // 2, espaco_y))
            espaco_y += 31

        pygame.display.flip()
        relogio.tick(FPS)