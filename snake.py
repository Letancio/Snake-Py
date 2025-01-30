import pygame
import random

# Inicializa o pygame
pygame.init()

# Configurações do jogo
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
SPEED = 10

# Cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Inicializa a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Cobrinha")

# Fonte
font = pygame.font.SysFont("arial", 20)
game_over_font = pygame.font.SysFont("arial", 30, bold=True)

# Função para desenhar a cobra
def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

# Função para exibir mensagem de game over
def show_game_over(score):
    text = game_over_font.render(f"Você perdeu: Pontuação foi: {score}", True, RED)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Mostra a mensagem por 3 segundos

# Função principal do jogo
def game_loop():
    clock = pygame.time.Clock()
    
    # Estado inicial
    snake_body = [[100, 100]]
    direction = "RIGHT"
    food_pos = [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]
    score = 0
    second_chance = False  # Controle para saber se já usou a segunda chance
    
    running = True
    while running:
        screen.fill(BLACK)

        # Eventos do teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # Movendo a cobra
        head = snake_body[-1].copy()
        if direction == "UP":
            head[1] -= BLOCK_SIZE
        elif direction == "DOWN":
            head[1] += BLOCK_SIZE
        elif direction == "LEFT":
            head[0] -= BLOCK_SIZE
        elif direction == "RIGHT":
            head[0] += BLOCK_SIZE

        # Verifica colisões
        if head in snake_body or head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            if score > 10 and not second_chance:
                second_chance = True  # Usa a segunda chance
                snake_body = [[100, 100]]  # Reinicia a cobra no canto
                direction = "RIGHT"  # Direção inicial
                continue  # Continua o jogo
            else:
                show_game_over(score)
                running = False  # Game Over

        # Adiciona a nova cabeça
        snake_body.append(head)

        # Se a cobra comer a comida
        if head == food_pos:
            food_pos = [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]
            score += 1  # Aumenta a pontuação
        else:
            snake_body.pop(0)

        # Desenha a comida
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

        # Desenha a cobra
        draw_snake(snake_body)

        # Mostra a pontuação
        score_text = font.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(SPEED)

    pygame.quit()

# Inicia o jogo
game_loop()
