import pygame
import sys
from src.constants import LARGURA_PADRAO, ALTURA_PADRAO, LARGURA_MP, ALTURA_MP
from src.telas import executar_menu, executar_instrucoes_solo, executar_instrucoes_multi
from src.jogo import rodar_jogo_1_player, rodar_jogo_2_players

def main():
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.set_num_channels(8)

    tela = pygame.display.set_mode((LARGURA_PADRAO, ALTURA_PADRAO))
    pygame.display.set_caption("Tetris")

    while True:
        tela = pygame.display.set_mode((LARGURA_PADRAO, ALTURA_PADRAO))
        escolha = executar_menu(tela)
        
        if escolha == 1:
            # Exibe a tela de instruções específica do modo solo sobre o fundo
            acao = executar_instrucoes_solo(tela)
            if acao == "menu":
                continue
            
            while True:
                resultado = rodar_jogo_1_player(tela)
                if resultado == "menu":
                    break
                elif resultado == "reiniciar":
                    continue
                    
        elif escolha == 2:
            tela = pygame.display.set_mode((LARGURA_MP, ALTURA_MP))
            # Exibe a tela de instruções específica do multiplayer sobre o fundo
            acao = executar_instrucoes_multi(tela)
            if acao == "menu":
                continue

            while True:
                resultado = rodar_jogo_2_players(tela)
                if resultado == "menu":
                    break
                elif resultado == "reiniciar":
                    continue

if __name__ == "__main__":
    main()