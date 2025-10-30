import pygame
import sys
import random

pygame.init()

# Размеры
CELL_SIZE = 24
COLS = 28
ROWS = 31
SCREEN_WIDTH = COLS * CELL_SIZE
SCREEN_HEIGHT = ROWS * CELL_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Цвета
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

# Упрощенный оригинальный лабиринт (0 - проход, 1 - стена)
maze_map = [
    "1111111111111111111111111111",
    "1000000000110000000000000001",
    "1011111110110111111111111101",
    "1011111110110111111111111101",
    "1011111110110111111111111101",
    "1000000000000000000000000001",
    "1011110111111111111111011101",
    "1000000110000000000110000001",
    "1111110110111111101101111111",
    "1111110110111111101101111111",
    "1111110110000000000111111111",
    "1111110110111111101101111111",
    "1111110110111111101101111111",
    "1000000000000000000000000001",
    "1011111110110111111111111101",
    "1000000110110110000000000001",
    "1111010110110110111111111101",
    "1000010000000000000000000101",
    "1011111111111111111111111101",
    "1000000000000000000000000001",
    "1111111111111111111111111111"
]

# Преобразование карты в список списков
def load_maze():
    return [[int(cell) for cell in row] for row in maze_map]

# Класс Pacman
class Pacman:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.speed = 1
        self.score = 0

    def pixel_pos(self):
        return (self.grid_x * CELL_SIZE + CELL_SIZE // 2, self.grid_y * CELL_SIZE + CELL_SIZE // 2)

    def move(self, maze):
        if self.can_move(maze, self.next_direction):
            self.direction = self.next_direction

        new_x = self.grid_x + self.direction[0]
        new_y = self.grid_y + self.direction[1]

        if self.can_move(maze, self.direction):
            self.grid_x = new_x
            self.grid_y = new_y

    def can_move(self, maze, direction):
        new_x = self.grid_x + direction[0]
        new_y = self.grid_y + direction[1]
        if 0 <= new_y < len(maze) and 0 <= new_x < len(maze[0]):
            return maze[new_y][new_x] == 0
        return False

    def draw(self):
        pygame.draw.circle(screen, YELLOW, self.pixel_pos(), CELL_SIZE // 2 - 2)

# Класс призрака
class Ghost:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        self.speed = 1

    def move(self, maze):
        new_x = self.grid_x + self.direction[0]
        new_y = self.grid_y + self.direction[1]

        if 0 <= new_y < len(maze) and 0 <= new_x < len(maze[0]) and maze[new_y][new_x] == 0:
            self.grid_x = new_x
            self.grid_y = new_y
        else:
            self.direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])

    def pixel_pos(self):
        return (self.grid_x * CELL_SIZE + CELL_SIZE // 2, self.grid_y * CELL_SIZE + CELL_SIZE // 2)

    def draw(self):
        pygame.draw.circle(screen, RED, self.pixel_pos(), CELL_SIZE // 2 - 2)

# Монеты
def generate_coins(maze):
    coins = set()
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 0:
                coins.add((x, y))
    return coins

def draw_maze(maze):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_coins(coins):
    for x, y in coins:
        pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 3)

def check_collision(pacman, ghosts):
    for ghost in ghosts:
        if pacman.grid_x == ghost.grid_x and pacman.grid_y == ghost.grid_y:
            return True
    return False

def game_loop():
    maze = load_maze()
    pacman = Pacman(1, 1)
    ghosts = [Ghost(26, 18), Ghost(1, 18)]  # Призраки по краям
    coins = generate_coins(maze)

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pacman.next_direction = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            pacman.next_direction = (1, 0)
        elif keys[pygame.K_UP]:
            pacman.next_direction = (0, -1)
        elif keys[pygame.K_DOWN]:
            pacman.next_direction = (0, 1)

        pacman.move(maze)

        if (pacman.grid_x, pacman.grid_y) in coins:
            coins.remove((pacman.grid_x, pacman.grid_y))
            pacman.score += 10

        for ghost in ghosts:
            ghost.move(maze)

        draw_maze(maze)
        draw_coins(coins)
        pacman.draw()
        for ghost in ghosts:
            ghost.draw()

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {pacman.score}", True, YELLOW)
        screen.blit(score_text, (10, 10))

        if check_collision(pacman, ghosts):
            game_over = font.render("Game Over!", True, RED)
            screen.blit(game_over, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        if len(coins) == 0:
            win_text = font.render("You Win!", True, YELLOW)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        pygame.display.update()
        clock.tick(10)

game_loop()
