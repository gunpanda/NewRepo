import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение параметров экрана
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Geometric Jump Game")

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Загрузка изображений
hero_image = pygame.image.load("cap_transparent.png")
background_image = pygame.image.load("c:\\code\\geometry\\fon.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Масштабируем фон

hero_width = 80
hero_height = 80
hero_image = pygame.transform.scale(hero_image, (hero_width, hero_height))

# Настройки главного героя (его начальные координаты и скорость)
hero_x = 100
hero_y = SCREEN_HEIGHT - 150
jump_speed = 20
gravity = 1

# Настройки игры
score = 0
font = pygame.font.Font(None, 74)

# Переменные для прыжка
is_jumping = False
jump_count = 0  # Счетчик прыжков
max_jumps = 2   # Максимальное количество прыжков

# Функция для генерации случайных препятствий
def generate_obstacle():
    shape_type = random.choice(['square', 'triangle', 'circle'])
    size = random.randint(30, 80)  # Размер фигуры
    x = SCREEN_WIDTH + size
    y = SCREEN_HEIGHT - size

    if shape_type == 'square':
        return 'square', pygame.Rect(x, y, size, size)
    elif shape_type == 'triangle':
        return 'triangle', (x, y, size)
    elif shape_type == 'circle':
        return 'circle', (x, y + size // 2, size // 2)

# Главная функция игры
def game():
    global hero_y, is_jumping, jump_count, jump_speed, score  # Declare jump_speed as global

    # Начальные параметры препятствий
    obstacles = []
    clock = pygame.time.Clock()
    spawn_delay = 1000  # Время появления новых препятствий
    last_spawn_time = pygame.time.get_ticks()
    
    # Параметры фона
    background_x = 0  # Начальная позиция фона

    running = True

    while running:
        # Движение фона
        background_x -= 5  # Скорость движения фона
        if background_x <= -SCREEN_WIDTH:
            background_x = 0  # Сброс позиции фона

        # Отображение фона
        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + SCREEN_WIDTH, 0))  # Повторяем фон

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Нажатие на пробел для прыжка
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not is_jumping:
                    is_jumping = True
                    jump_count = 1  # Сброс счетчика прыжков
                elif jump_count < max_jumps:
                    jump_count += 1  # Увеличение счетчика для двойного прыжка

        # Обработка прыжка
        if is_jumping:
            hero_y -= jump_speed
            jump_speed -= gravity
            if hero_y >= SCREEN_HEIGHT - 150:
                hero_y = SCREEN_HEIGHT - 150
                is_jumping = False
                jump_count = 0  # Сброс счетчика прыжков
                jump_speed = 20  # Сброс скорости прыжка
        else:
            # Если не прыгаем, то герой не уходит ниже начальной позиции
            if hero_y < SCREEN_HEIGHT - 150:
                hero_y += gravity

        # Движение препятствий
        if pygame.time.get_ticks() - last_spawn_time > spawn_delay:
            obstacles.append(generate_obstacle())
            last_spawn_time = pygame.time.get_ticks()

        # Обновление позиции препятствий
        for i in range(len(obstacles)):
            shape_type, obstacle = obstacles[i]
            if shape_type == 'square':
                obstacle.x -= 5  # Двигаем препятствие влево
            elif shape_type == 'triangle':
                x, y, size = obstacle
                obstacle = (x - 5, y, size)  # Двигаем треугольник влево
                obstacles[i] = (shape_type, obstacle)
            elif shape_type == 'circle':
                circle_x, circle_y, radius = obstacle
                obstacle = (circle_x - 5, circle_y, radius)  # Двигаем круг влево
                obstacles[i] = (shape_type, obstacle)

        # Отображение главного героя
        screen.blit(hero_image, (hero_x, hero_y))

        # Отображение препятствий
        for shape_type, obstacle in obstacles:
            if shape_type == 'square':
                pygame.draw.rect(screen, (255, 0, 0), obstacle)
            elif shape_type == 'triangle':
                x, y, size = obstacle
                points = [(x, y), (x - size // 2, y + size), (x + size // 2, y + size)]
                pygame.draw.polygon(screen, (0, 255, 0), points)
            elif shape_type == 'circle':
                pygame.draw.circle(screen, (0, 0, 255), obstacle[:2], obstacle[2])

            # Проверка на столкновение
            if shape_type == 'square' and hero_x + hero_width > obstacle.x and hero_x < obstacle.x + obstacle.width:
                if hero_y + hero_height > obstacle.y:
                    running = False  # Завершаем игру при столкновении
            elif shape_type == 'triangle':
                x, y, size = obstacle
                if hero_x + hero_width > x - size // 2 and hero_x < x + size // 2:
                    if hero_y + hero_height > y:
                        running = False
            elif shape_type == 'circle':
                circle_x, circle_y, radius = obstacle
                if (hero_x - circle_x) ** 2 + (hero_y + hero_height - circle_y) ** 2 < radius ** 2:
                    running = False

        # Отображение счета
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (50, 50))

        pygame.display.flip()
        clock.tick(60)

# Запуск игры
if __name__ == "__main__":
    game()

pygame.quit()
