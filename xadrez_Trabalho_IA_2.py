import pygame
import sys
import random

# Configurações
TAM_CELULA = 60
NUM_RAINHAS = 8
LARGURA = TAM_CELULA * NUM_RAINHAS
ALTURA = TAM_CELULA * NUM_RAINHAS + 60  # espaço extra para os botões

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Problema das 8 Rainhas")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (200, 200, 200)

# Fonte
font = pygame.font.SysFont(None, 30)

# Variável da solução atual
solucao = []

# Backtracking
def existe_conflict(col, row, solucao):
    for c in range(col):
        r = solucao[c]
        if r == row or abs(r - row) == abs(c - col):
            return True
    return False

def gerar_solucao_recursive(col, solucao_atual):
    if col == NUM_RAINHAS:
        return solucao_atual[:]
    options = [row for row in range(NUM_RAINHAS) if not existe_conflict(col, row, solucao_atual)]
    random.shuffle(options)
    for row in options:
        solucao_atual.append(row)
        resultado = gerar_solucao_recursive(col + 1, solucao_atual)
        if resultado:
            return resultado
        solucao_atual.pop()
    return None

def gerar_solucao():
    return gerar_solucao_recursive(0, [])

# Random Restart
def conflitos(tabuleiro):
    confl = 0
    for i in range(NUM_RAINHAS):
        for j in range(i + 1, NUM_RAINHAS):
            if tabuleiro[i] == tabuleiro[j] or abs(tabuleiro[i] - tabuleiro[j]) == abs(i - j):
                confl += 1
    return confl

def busca_aleatoria_com_repeticoes():
    while True:
        tentativa = [random.randint(0, NUM_RAINHAS - 1) for _ in range(NUM_RAINHAS)]
        if conflitos(tentativa) == 0:
            return tentativa

# Algoritmo Genético
def fitness(individuo):
    return 28 - conflitos(individuo)

def crossover(pai1, pai2):
    ponto = random.randint(1, NUM_RAINHAS - 2)
    return pai1[:ponto] + pai2[ponto:]

def mutacao(individuo, taxa=0.2):
    if random.random() < taxa:
        i = random.randint(0, NUM_RAINHAS - 1)
        individuo[i] = random.randint(0, NUM_RAINHAS - 1)
    return individuo

def algoritmo_genetico(pop_tam=100, geracoes=1000):
    populacao = [[random.randint(0, NUM_RAINHAS - 1) for _ in range(NUM_RAINHAS)] for _ in range(pop_tam)]
    for _ in range(geracoes):
        populacao.sort(key=fitness, reverse=True)
        if fitness(populacao[0]) == 28:
            return populacao[0]
        nova_populacao = populacao[:10]
        while len(nova_populacao) < pop_tam:
            pai1, pai2 = random.choices(populacao[:50], k=2)
            filho = crossover(pai1, pai2)
            filho = mutacao(filho)
            nova_populacao.append(filho)
        populacao = nova_populacao
    return populacao[0]

# Desenho
def desenhar_tabuleiro():
    for linha in range(NUM_RAINHAS):
        for coluna in range(NUM_RAINHAS):
            cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
            rect = pygame.Rect(coluna * TAM_CELULA, linha * TAM_CELULA, TAM_CELULA, TAM_CELULA)
            pygame.draw.rect(screen, cor, rect)

def desenhar_rainhas():
    for coluna, linha in enumerate(solucao):
        center_x = coluna * TAM_CELULA + TAM_CELULA // 2
        center_y = linha * TAM_CELULA + TAM_CELULA // 2
        radius = TAM_CELULA // 3
        pygame.draw.circle(screen, VERMELHO, (center_x, center_y), radius)

def desenhar_botoes():
    botoes = []
    textos = ["Backtracking", "Random Restart", "Alg. Genético"]
    for i, texto in enumerate(textos):
        largura = 153
        altura = 40
        x = 10 + i * (largura + 10)
        y = ALTURA - 50
        rect = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(screen, AZUL, rect)
        texto_render = font.render(texto, True, BRANCO)
        texto_rect = texto_render.get_rect(center=rect.center)
        screen.blit(texto_render, texto_rect)
        botoes.append((rect, texto))
    return botoes

# Loop principal
def main():
    global solucao
    clock = pygame.time.Clock()
    solucao = gerar_solucao()

    while True:
        screen.fill(CINZA)
        botoes = desenhar_botoes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, nome in botoes:
                    if rect.collidepoint(mouse_pos):
                        if nome == "Backtracking":
                            solucao = gerar_solucao()
                        elif nome == "Random Restart":
                            solucao = busca_aleatoria_com_repeticoes()
                        elif nome == "Alg. Genético":
                            solucao = algoritmo_genetico()

        desenhar_tabuleiro()
        desenhar_rainhas()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
