import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размер экрана и ячейки
CELL_SIZE = 32
SCREEN_WIDTH = 448
SCREEN_HEIGHT = 576
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman")

# Цвета
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Лабиринт
ROWS = SCREEN_HEIGHT // CELL_SIZE
COLS = SCREEN_WIDTH // CELL_SIZE

# ФПС
clock = pygame.time.Clock()

# Класс Pacman
class Pacman:
    def __init__(self):
        self.x = CELL_SIZE
        self.y = CELL_SIZE
        self.speed = 4
        self.score = 0

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x + CELL_SIZE // 2, self.y + CELL_SIZE // 2), 16)

    def move(self, dx, dy, maze):
        if maze[(self.y + dy * self.speed) // CELL_SIZE][(self.x + dx * self.speed) // CELL_SIZE] == 0:
            self.x += dx * self.speed
            self.y += dy * self.speed

    def eat_coin(self, coins):
        pos = (self.x // CELL_SIZE, self.y // CELL_SIZE)
        if pos in coins:
            coins.remove(pos)
            self.score += 1

class Ghost:
    def __init__(self):
        self.x = random.randint(1, COLS - 2) * CELL_SIZE  # Начальное положение внутри границ
        self.y = random.randint(1, ROWS - 2) * CELL_SIZE
        self.speed = 2
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])  # направления: вправо, влево, вниз, вверх

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x + CELL_SIZE // 2, self.y + CELL_SIZE // 2), 16)

    def move(self, maze):
        dx, dy = self.direction
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Проверка, что новые координаты находятся в пределах индексов массива
        if 0 <= new_y // CELL_SIZE < len(maze) and 0 <= new_x // CELL_SIZE < len(maze[0]):
            if maze[new_y // CELL_SIZE][new_x // CELL_SIZE] == 0:
                self.x = new_x
                self.y = new_y
            else:
                # Если натолкнулся на стену, меняем направление
                self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        else:
            # Если выходит за границы лабиринта, меняем направление
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

# Предопределённый лабиринт
def generate_maze():
    # 1 - стена, 0 - проход
    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    return maze

# Создание монет в проходах лабиринта
def create_coins(maze):
    coins = set()
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 0:
                coins.add((col, row))
    return coins

# Отрисовка лабиринта
def draw_maze(maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Отрисовка монет
def draw_coins(coins):
    for coin in coins:
        pygame.draw.circle(screen, WHITE, (coin[0] * CELL_SIZE + CELL_SIZE // 2, coin[1] * CELL_SIZE + CELL_SIZE // 2), 4)

# Проверка на столкновение с призраком
def check_collision(pacman, ghosts):
    for ghost in ghosts:
        if pacman.x // CELL_SIZE == ghost.x // CELL_SIZE and pacman.y // CELL_SIZE == ghost.y // CELL_SIZE:
            return True
    return False

# Проверка, все ли монеты собраны
def check_all_coins_collected(coins):
    return len(coins) == 0

# Основная функция игры
def game_loop():
    maze = generate_maze()
    coins = create_coins(maze)
    pacman = Pacman()
    ghosts = [Ghost() for _ in range(2)]  # создаем 2 призрака

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Управление Pacman'ом
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1

        # Обновление позиции Pacman'а
        pacman.move(dx, dy, maze)
        pacman.eat_coin(coins)

        # Проверка на победу
        if check_all_coins_collected(coins):
            font = pygame.font.Font(None, 72)
            win_text = font.render("You Win!", True, YELLOW)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        # Проверка на столкновение с призраком
        if check_collision(pacman, ghosts):
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        # Обновление позиции призраков
        for ghost in ghosts:
            ghost.move(maze)

        # Рендеринг
        screen.fill(BLACK)
        draw_maze(maze)
        draw_coins(coins)
        pacman.draw()
        for ghost in ghosts:
            ghost.draw()

        # Отображение счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {pacman.score}", True, YELLOW)
        screen.blit(score_text, (10, 10))

        pygame.display.update()

        # Ограничение FPS
        clock.tick(60)

# Запуск игры
game_loop()
