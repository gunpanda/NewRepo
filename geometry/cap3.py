import pygame
import random

# Инициализация Pygame
pygame.init()

# Установка режима экрана
screen_width = 1600  # Ширина экрана под фон
screen_height = 1043  # Высота экрана под фон
screen = pygame.display.set_mode((screen_width, screen_height))

# Загрузка фонового изображения и его обработка
background = pygame.image.load("c:\\code\\geometry\\fon.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# Функция для загрузки и обработки спрайтов
def load_sprite(path, size=(128, 256)):  # Размер спрайта героя
    sprite = pygame.image.load(path).convert_alpha()  # Загружаем изображение с альфа-каналом
    return pygame.transform.scale(sprite, size)  # Изменяем размер спрайта

# Загрузка спрайтов
sprites = [
    load_sprite("c:\\code\\geometry\\cap_sprite_1.png"),
    load_sprite("c:\\code\\geometry\\cap_sprite_2.png"),
    load_sprite("c:\\code\\geometry\\cap_sprite_3.png"),
    load_sprite("c:\\code\\geometry\\cap_sprite_4.png")
]

# Параметры игры
hero_x = 100
hero_y = 680  # Устанавливаем положение героя чуть выше
gravity = 0.5
jump_speed = 15
speed = 10
hero_speed_y = 0
is_jumping = False
double_jump = False
score = 0
frame_count = 0  # Для анимации
sprite_index = 0  # Индекс текущего спрайта

# Список препятствий
obstacle = None
obstacle_shape = None

# Функция для создания нового препятствия
def create_obstacle():
    global obstacle_shape
    shape_type = random.choice(['rectangle', 'circle', 'triangle'])  # Выбираем случайную форму
    if shape_type == 'rectangle':
        width = random.randint(50, 150)
        height = random.randint(30, 50)  # Высота препятствия меньше, чтобы не задевать героя
        obstacle = pygame.Rect(screen_width, 680 - height, width, height)  # Опускаем препятствие ниже
        obstacle_shape = 'rectangle'
        return obstacle
    elif shape_type == 'circle':
        radius = random.randint(30, 50)
        obstacle = pygame.Rect(screen_width, 680 - radius, radius * 2, radius * 2)  # Опускаем круг ниже
        obstacle_shape = 'circle'
        return obstacle
    elif shape_type == 'triangle':
        size = random.randint(50, 100)
        obstacle = pygame.Rect(screen_width, 680 - size, size, size)  # Опускаем треугольник ниже
        obstacle_shape = 'triangle'
        return obstacle

# Запуск музыки
pygame.mixer.music.load("c:\\code\\geometry\\mu.mp3")  # Загрузка музыкального файла
pygame.mixer.music.play(-1)  # Воспроизведение музыки в цикле

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

# Создание первого препятствия
obstacle = create_obstacle()

# Параметры движения фона
background_x1 = 0
background_x2 = screen_width

while running:
    clock.tick(60)  # Ограничение FPS до 60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not is_jumping:
                    is_jumping = True
                    hero_speed_y = -jump_speed
                elif not double_jump:
                    double_jump = True
                    hero_speed_y = -jump_speed

    # Обновление позиции героя
    if is_jumping:
        hero_y += hero_speed_y
        hero_speed_y += gravity  # Применяем гравитацию

        # Проверка на приземление
        if hero_y >= 680:  # Проверяем, чтобы герой не падал ниже 550
            hero_y = 680
            is_jumping = False
            double_jump = False
            hero_speed_y = 0

    # Двигаем препятствие влево
    if obstacle:
        obstacle.x -= speed  # Двигаем препятствия влево

        if obstacle.x < 0:  # Удаляем препятствие, если оно вышло за экран
            score += 1  # Увеличиваем счет
            obstacle = create_obstacle()  # Создаем новое препятствие

    # Проверка столкновений
    hero_rect = pygame.Rect(hero_x, hero_y, sprites[0].get_width(), sprites[0].get_height())
    if obstacle and hero_rect.colliderect(obstacle.inflate(-20, -20)):  # Уменьшаем область столкновения
        running = False  # Завершаем игру

    # Анимация героя
    frame_count += 1
    if frame_count >= 10:  # Меняем спрайт каждые 10 кадров
        sprite_index = (sprite_index + 1) % len(sprites)
        frame_count = 0

    # Обновление фона
    background_x1 -= speed * 0.5  # Двигаем фон с меньшей скоростью
    background_x2 -= speed * 0.5

    # Если фон ушел за пределы экрана, перемещаем его в начало
    if background_x1 <= -screen_width:
        background_x1 = screen_width
    if background_x2 <= -screen_width:
        background_x2 = screen_width

    # Отображение
    screen.blit(background, (background_x1, 0))  # Отображаем фон
    screen.blit(background, (background_x2, 0))  # Отображаем фон
    screen.blit(sprites[sprite_index], (hero_x, hero_y))  # Отображаем героя с анимацией

    # Отображение препятствия
    if obstacle:
        if obstacle_shape == 'rectangle':
            pygame.draw.rect(screen, (255, 0, 0), obstacle)  # Отображаем прямоугольник
        elif obstacle_shape == 'circle':
            pygame.draw.circle(screen, (0, 255, 0), (obstacle.centerx, obstacle.centery), obstacle.width // 2)  # Отображаем круг
        elif obstacle_shape == 'triangle':
            size = obstacle.width  # Используем ширину как размер
            points = [(obstacle.x, obstacle.y + size), (obstacle.x + size // 2, obstacle.y), (obstacle.x + size, obstacle.y + size)]
            pygame.draw.polygon(screen, (0, 0, 255), points)  # Отображаем треугольник

    # Отображение счета
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
