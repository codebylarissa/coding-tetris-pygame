# Tetris em Pygame

Um jogo clássico de Tetris desenvolvido em Python utilizando a biblioteca Pygame.


## Como Executar o Projeto

### Pré-requisitos
Certifique-se de que tem o Python instalado na sua máquina. Você também vai precisar da biblioteca **Pygame**.

1. Clone o repositório ou baixe os arquivos do projeto.
2. Instale o Pygame executando o seguinte comando no seu terminal:
   ```bash
   pip install pygame
   ```

### Executando o Jogo
Navegue até a pasta raiz do projeto e execute o arquivo principal (`main.py`):
```bash
python main.py
```

## Estrutura do Projeto
```
coding-tetris-pygame/
├── assets/                                 # Recursos visuais (imagens, ícones) do jogo
├── fonts/                                  # Fontes personalizadas utilizadas no jogo
├── sounds/                                 # Efeitos sonoros e músicas do jogo
├── src/                                    # Pasta principal contendo os módulos do código
│   ├── init.py                             # Arquivo de marcação que define o diretório como um pacote Python
│   ├── constants.py                        # Configurações, cores e constantes globais do jogo
│   ├── jogo.py                             # Lógica principal do loop e funcionamento da partida
│   ├── tabuleiro.py                        # Regras de posicionamento e controle da matriz do tabuleiro
│   └── telas.py                            # Gestão de telas, menus e estados visuais (como o pause)
├── .gitignore                              # Arquivos e pastas ignorados pelo Git
├── main.py                                 # Ponto de entrada (entry point) responsável por iniciar o jogo
└── README.md                               # Documentação do projeto
```