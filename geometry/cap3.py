import pygame
import random

# Инициализация Pygame
pygame.init()

# Установка режима экрана
screen_width = 1600
screen_height = 1043
screen = pygame.display.set_mode((screen_width, screen_height))

# Загрузка фонового изображения
background = pygame.image.load("c:\\code\\geometry\\fon.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# Загрузка и обработка спрайтов
def load_sprite(path, size=(178, 196)):
    sprite = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(sprite, size)

# Загрузка спрайтов препятствий
obstacle_sprites = [
    load_sprite("c:\\code\\geometry\\obstacle_sprite1.png", (178, 196)),
    load_sprite("c:\\code\\geometry\\obstacle_sprite2.png", (178, 196)),
    load_sprite("c:\\code\\geometry\\obstacle_sprite3.png", (178, 196))
]

# Загрузка спрайтов героя
hero_sprites = [
    load_sprite("c:\\code\\geometry\\cap_sprite_1.png", (128, 256)),
    load_sprite("c:\\code\\geometry\\cap_sprite_2.png", (128, 256)),
    load_sprite("c:\\code\\geometry\\cap_sprite_3.png", (128, 256)),
    load_sprite("c:\\code\\geometry\\cap_sprite_4.png", (128, 256))
]

# Загрузка спрайтов монет
coin_sprites = [
    load_sprite("c:\\code\\geometry\\coin_sprite1.png", (50, 50)),
    load_sprite("c:\\code\\geometry\\coin_sprite2.png", (50, 50)),
    load_sprite("c:\\code\\geometry\\coin_sprite3.png", (50, 50))
]

# Параметры игры
hero_x = 100
hero_y = 680  # Позиция героя на экране
gravity = 0.5
jump_speed = 15
speed = 10
hero_speed_y = 0
is_jumping = False
double_jump = False
lives = 3  # Количество жизней
game_over = False  # Флаг окончания игры
score = 0
frame_count = 0
hero_frame_count = 0
coin_frame_count = 0
obstacle_index = 0  # Индекс текущего спрайта препятствия
hero_sprite_index = 0  # Индекс текущего спрайта героя
coin_sprite_index = 0  # Индекс текущего спрайта монет
background_x1 = 0
background_x2 = screen_width

# Список препятствий и монет
obstacle = None
coin = None

# Функция для создания препятствия на уровне героя
def create_obstacle():
    obstacle_height = random.randint(50, 150)  # Высота препятствия, чтобы оно было ниже героя
    obstacle_y = 680 - obstacle_height  # Чтобы оно всегда было преодолимо
    return pygame.Rect(screen_width, obstacle_y, 178, obstacle_height)

# Функция для создания монет
def create_coin():
    while True:
        coin_rect = pygame.Rect(random.randint(screen_width, screen_width + 400), random.randint(400, 650), 50, 50)
        if not obstacle.colliderect(coin_rect):  # Проверяем, чтобы монета не пересекалась с препятствием
            return coin_rect

# Функция для отображения текста
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

# Создание первого препятствия и монетки
obstacle = create_obstacle()
coin = create_coin()

# Запуск музыки
pygame.mixer.music.load("c:\\code\\geometry\\mu.mp3")
pygame.mixer.music.play(-1)

while running:
    clock.tick(60)  # Ограничение FPS до 60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                if not is_jumping:
                    is_jumping = True
                    hero_speed_y = -jump_speed
                elif not double_jump:
                    double_jump = True
                    hero_speed_y = -jump_speed

    if not game_over:
        # Обновление позиции героя
        if is_jumping:
            hero_y += hero_speed_y
            hero_speed_y += gravity
            if hero_y >= 680:
                hero_y = 680
                is_jumping = False
                double_jump = False
                hero_speed_y = 0

        # Двигаем препятствия и монетки
        obstacle.x -= speed
        coin.x -= speed

        # Если препятствие вышло за экран, создаем новое
        if obstacle.x < -178:
            score += 1
            obstacle = create_obstacle()
            coin = create_coin()  # Новая монета при каждом новом препятствии

        # Проверка столкновений (уменьшаем зоны столкновения)
        hero_rect = pygame.Rect(hero_x, hero_y, 128, 256).inflate(-20, -20)  # Уменьшаем зону героя
        obstacle_rect = obstacle.inflate(-30, -30)  # Уменьшаем зону препятствия

        if hero_rect.colliderect(obstacle_rect):
            lives -= 1  # Уменьшаем количество жизней
            if lives == 0:
                game_over = True  # Игра окончена, если жизни закончились
            else:
                obstacle = create_obstacle()  # Если есть жизни, создаем новое препятствие

        # Проверка на сбор монетки
        if hero_rect.colliderect(coin):
            score += 5  # Очки за монетку
            coin = create_coin()

        # Анимация препятствий
        frame_count += 1
        if frame_count >= 10:
            obstacle_index = (obstacle_index + 1) % len(obstacle_sprites)
            frame_count = 0

        # Анимация героя
        hero_frame_count += 1
        if hero_frame_count >= 10:
            hero_sprite_index = (hero_sprite_index + 1) % len(hero_sprites)
            hero_frame_count = 0

        # Анимация монет
        coin_frame_count += 1
        if coin_frame_count >= 10:
            coin_sprite_index = (coin_sprite_index + 1) % len(coin_sprites)
            coin_frame_count = 0

        # Обновление фона
        background_x1 -= speed * 0.5
        background_x2 -= speed * 0.5
        if background_x1 <= -screen_width:
            background_x1 = screen_width
        if background_x2 <= -screen_width:
            background_x2 = screen_width

        # Отображение элементов игры
        screen.blit(background, (background_x1, 0))
        screen.blit(background, (background_x2, 0))
        screen.blit(obstacle_sprites[obstacle_index], obstacle)
        screen.blit(coin_sprites[coin_sprite_index], coin)  # Отображение анимированной монеты
        screen.blit(hero_sprites[hero_sprite_index], (hero_x, hero_y))  # Отображение анимированного героя

        # Отображение счета и жизней
        draw_text(f'Score: {score}', 36, (255, 255, 255), 10, 10)
        draw_text(f'Lives: {lives}', 36, (255, 255, 255), 10, 50)

    else:
        # Экран Game Over
        draw_text('Game Over', 100, (255, 0, 0), screen_width // 2 - 200, screen_height // 2 - 50)
        draw_text(f'Score: {score}', 50, (255, 255, 255), screen_width // 2 - 100, screen_height // 2 + 50)

    pygame.display.flip()

pygame.quit()
