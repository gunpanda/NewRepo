import pygame
import random
import sys

# Инициализация Pygame
pygame.init()
pygame.mixer.init() # Для звуков (если захотим добавить)

# --- Константы ---
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 540 # Делаем немного не квадратным, чтобы влез счет
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - 60) // GRID_SIZE # Оставляем место для счета вверху

# Цвета (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)      # Яркий зеленый для змейки
DARK_GREEN = (0, 100, 0)   # Темно-зеленый для головы или тени
RED = (220, 20, 60)        # Красный для еды
LIGHT_RED = (255, 99, 71)  # Светлее для анимации еды
BACKGROUND_COLOR = (40, 40, 60) # Темно-сине-серый фон
GRID_COLOR = (50, 50, 70)   # Цвет сетки, чуть светлее фона
TEXT_COLOR = (200, 200, 220) # Цвет текста
GAME_OVER_COLOR = (180, 0, 0)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Шрифты
SCORE_FONT = pygame.font.SysFont("consolas", 30, bold=True)
GAME_OVER_FONT = pygame.font.SysFont("impact", 70) # Более "игровой" шрифт
INFO_FONT = pygame.font.SysFont("consolas", 20)

# --- Настройка экрана ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Красивая Змейка")
clock = pygame.time.Clock()

# --- Вспомогательные функции ---
def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 60), (x, SCREEN_HEIGHT)) # Начинаем сетку ниже области счета
    for y in range(60, SCREEN_HEIGHT, GRID_SIZE): # Начинаем сетку ниже области счета
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

def draw_rounded_rect(surface, color, rect, radius, border=0):
    """Рисует прямоугольник со скругленными углами."""
    pygame.draw.rect(surface, color, rect, border, border_radius=radius)

def get_eye_positions(head_pos, direction):
    """Возвращает позиции глаз в зависимости от направления."""
    eye_offset_x = GRID_SIZE // 4
    eye_offset_y = GRID_SIZE // 4
    eye_size = GRID_SIZE // 6

    if direction == UP:
        left_eye = (head_pos[0] * GRID_SIZE + eye_offset_x, head_pos[1] * GRID_SIZE + eye_offset_y)
        right_eye = (head_pos[0] * GRID_SIZE + GRID_SIZE - eye_offset_x - eye_size, head_pos[1] * GRID_SIZE + eye_offset_y)
    elif direction == DOWN:
        left_eye = (head_pos[0] * GRID_SIZE + eye_offset_x, head_pos[1] * GRID_SIZE + GRID_SIZE - eye_offset_y - eye_size)
        right_eye = (head_pos[0] * GRID_SIZE + GRID_SIZE - eye_offset_x - eye_size, head_pos[1] * GRID_SIZE + GRID_SIZE - eye_offset_y - eye_size)
    elif direction == LEFT:
        left_eye = (head_pos[0] * GRID_SIZE + eye_offset_x, head_pos[1] * GRID_SIZE + eye_offset_y)
        right_eye = (head_pos[0] * GRID_SIZE + eye_offset_x, head_pos[1] * GRID_SIZE + GRID_SIZE - eye_offset_y - eye_size)
    else:  # RIGHT
        left_eye = (head_pos[0] * GRID_SIZE + GRID_SIZE - eye_offset_x - eye_size, head_pos[1] * GRID_SIZE + eye_offset_y)
        right_eye = (head_pos[0] * GRID_SIZE + GRID_SIZE - eye_offset_x - eye_size, head_pos[1] * GRID_SIZE + GRID_SIZE - eye_offset_y - eye_size)
    
    # Смещаем глаза на область счета
    left_eye = (left_eye[0], left_eye[1] + 60)
    right_eye = (right_eye[0], right_eye[1] + 60)
    
    return left_eye, right_eye, eye_size


# --- Классы ---
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))] # Начальная позиция в центре
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.head_color = DARK_GREEN
        self.score = 0
        self.growing = False # Флаг для роста змейки, чтобы не удалять хвост сразу

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return # Нельзя развернуться на 180 градусов
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + x) % GRID_WIDTH), ((cur[1] + y) % GRID_HEIGHT)) # % для прохода сквозь стены

        # Проверка на столкновение с собой
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True # Game Over

        self.positions.insert(0, new)
        if self.growing:
            self.growing = False
        else:
            self.positions.pop()
        return False # No collision

    def grow(self):
        self.growing = True
        self.score += 1

    def draw(self, surface):
        # Тело змейки
        for i, p in enumerate(self.positions):
            r = pygame.Rect((p[0] * GRID_SIZE), (p[1] * GRID_SIZE + 60), GRID_SIZE, GRID_SIZE) # +60 для смещения под счет
            if i == 0: # Голова
                draw_rounded_rect(surface, self.head_color, r, GRID_SIZE // 3)
                # Глаза
                eye_pos1, eye_pos2, eye_size = get_eye_positions(p, self.direction)
                pygame.draw.circle(surface, WHITE, (eye_pos1[0] + eye_size//2, eye_pos1[1] + eye_size//2), eye_size)
                pygame.draw.circle(surface, WHITE, (eye_pos2[0] + eye_size//2, eye_pos2[1] + eye_size//2), eye_size)
                pygame.draw.circle(surface, BLACK, (eye_pos1[0] + eye_size//2, eye_pos1[1] + eye_size//2), eye_size // 2)
                pygame.draw.circle(surface, BLACK, (eye_pos2[0] + eye_size//2, eye_pos2[1] + eye_size//2), eye_size // 2)

            else: # Сегменты тела
                # Градиент для тела (опционально, можно просто self.color)
                # Чем дальше от головы, тем темнее (или светлее)
                body_shade = min(255, max(0, self.color[1] - i * 5)) # Уменьшаем зеленую компоненту
                body_color = (self.color[0], body_shade, self.color[2])
                draw_rounded_rect(surface, body_color, r, GRID_SIZE // 4)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.light_color = LIGHT_RED
        self.pulse_timer = 0
        self.pulse_speed = 0.1 # Скорость пульсации
        self.randomize_position([]) # Первоначальное размещение

    def randomize_position(self, snake_positions):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions:
                break

    def draw(self, surface):
        self.pulse_timer += self.pulse_speed
        # Пульсация размера или цвета
        # Для простоты, будем немного менять цвет или рисовать "сияние"
        r = pygame.Rect((self.position[0] * GRID_SIZE), (self.position[1] * GRID_SIZE + 60), GRID_SIZE, GRID_SIZE) # +60
        
        # Анимация "сияния"
        pulse_radius_factor = abs(pygame.math.Vector2(1,0).rotate_rad(self.pulse_timer).y) # от 0 до 1
        outer_radius = int(GRID_SIZE * (0.4 + 0.1 * pulse_radius_factor))
        inner_radius = int(GRID_SIZE * 0.3)

        center_x = r.left + GRID_SIZE // 2
        center_y = r.top + GRID_SIZE // 2

        pygame.draw.circle(surface, self.light_color, (center_x, center_y), outer_radius)
        pygame.draw.circle(surface, self.color, (center_x, center_y), inner_radius)


# --- Основная функция игры ---
def game_loop():
    snake = Snake()
    food = Food()
    food.randomize_position(snake.positions)

    game_over = False
    paused = False
    
    # Скорость игры (количество кадров в секунду, влияющее на скорость змейки)
    # Чем меньше значение, тем медленнее змейка (т.к. мы обновляем ее положение реже)
    # Вместо FPS, будем использовать таймер для движения
    snake_speed = 150 # миллисекунд на ход
    last_move_time = pygame.time.get_ticks()

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r: # Рестарт
                        return # Начать новую игру
                    if event.key == pygame.K_q: # Выход
                        running = False
                        pygame.quit()
                        sys.exit()
                else: # Если не Game Over
                    if event.key == pygame.K_p:
                        paused = not paused
                    if not paused:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            snake.turn(UP)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            snake.turn(DOWN)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            snake.turn(LEFT)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            snake.turn(RIGHT)

        if not game_over and not paused:
            if current_time - last_move_time > snake_speed:
                collision_with_self = snake.move()
                if collision_with_self: # Проверка на столкновение с собой
                    game_over = True
                
                last_move_time = current_time

                # Проверка на съедение еды
                if snake.get_head_position() == food.position:
                    snake.grow()
                    food.randomize_position(snake.positions)
                    # Увеличиваем скорость немного
                    snake_speed = max(50, snake_speed * 0.98)


        # --- Отрисовка ---
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        
        snake.draw(screen)
        food.draw(screen)

        # Отображение счета
        score_text = SCORE_FONT.render(f"Счет: {snake.score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

        if paused and not game_over:
            pause_surf = GAME_OVER_FONT.render("ПАУЗА", True, TEXT_COLOR)
            pause_rect = pause_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(pause_surf, pause_rect)
            
            info_surf_pause = INFO_FONT.render("Нажмите P чтобы продолжить", True, TEXT_COLOR)
            info_rect_pause = info_surf_pause.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))
            screen.blit(info_surf_pause, info_rect_pause)

        if game_over:
            # Затемнение экрана
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) # Черный с прозрачностью
            screen.blit(overlay, (0,0))

            game_over_surf = GAME_OVER_FONT.render("ИГРА ОКОНЧЕНА", True, GAME_OVER_COLOR)
            game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
            screen.blit(game_over_surf, game_over_rect)

            final_score_surf = SCORE_FONT.render(f"Ваш счет: {snake.score}", True, TEXT_COLOR)
            final_score_rect = final_score_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
            screen.blit(final_score_surf, final_score_rect)
            
            info_surf = INFO_FONT.render("Нажмите R чтобы начать заново, Q чтобы выйти", True, TEXT_COLOR)
            info_rect = info_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 70))
            screen.blit(info_surf, info_rect)


        pygame.display.flip() # Обновляем весь экран
        clock.tick(30) # Ограничиваем FPS до 30 (для анимации еды, не для скорости змейки)
    
    pygame.quit()
    sys.exit()


# --- Запуск игры ---
if __name__ == '__main__':
    while True: # Позволяет перезапускать игру
        game_loop()