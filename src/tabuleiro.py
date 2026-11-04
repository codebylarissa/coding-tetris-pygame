from src.constants import FORMATOS_PECAS

class Tabuleiro:
    def __init__(self, colunas=10, linhas=21):
        self.colunas = colunas
        self.linhas = linhas
        self.grid = [[0 for _ in range(colunas)] for _ in range(linhas)]

    def reiniciar(self):
        self.grid = [[0 for _ in range(self.colunas)] for _ in range(self.linhas)]

    def obter_posicoes_peca(self, coluna, linha, tipo, rotacao):
        formato = FORMATOS_PECAS[tipo][rotacao]
        posicoes = []
        for bloco in formato:
            deslocamento_x = bloco % 4
            deslocamento_y = bloco // 4
            posicoes.append((coluna + deslocamento_x, linha + deslocamento_y))
        return posicoes

    def posicao_valida(self, coluna, linha, tipo, rotacao):
        for col, lin in self.obter_posicoes_peca(coluna, linha, tipo, rotacao):
            if col < 0 or col >= self.colunas or lin >= self.linhas:
                return False
            if lin >= 0 and self.grid[lin][col] != 0:
                return False
        return True

    def travar_peca(self, coluna, linha, tipo, rotacao):
        """Trava a peça no grid. Retorna True se travou com sucesso, ou False se estourou o topo (Game Over)."""
        jogo_perdido = False
        for col, lin in self.obter_posicoes_peca(coluna, linha, tipo, rotacao):
            if lin >= 0:
                self.grid[lin][col] = 1
            else:
                jogo_perdido = True
        return not jogo_perdido

    def limpar_linhas(self):
        """Remove linhas completas, atualiza o grid e retorna o número de linhas removidas."""
        novas_linhas = [linha for linha in self.grid if any(celula == 0 for celula in linha)]
        linhas_removidas = self.linhas - len(novas_linhas)
        
        if linhas_removidas > 0:
            linhas_vazias = [[0 for _ in range(self.colunas)] for _ in range(linhas_removidas)]
            self.grid = linhas_vazias + novas_linhas
            
        return linhas_removidas