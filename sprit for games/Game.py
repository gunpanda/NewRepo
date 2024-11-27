import pygame
import os

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер")

# Загрузка изображения
def load_image(folder, filename):
    return pygame.image.load(os.path.join(folder, filename)).convert_alpha()

# Папки с текстурами
BASE_FOLDER = r'C:\code\sprit for games'
PLAYER_FOLDER = os.path.join(BASE_FOLDER, 'Player', 'p1_walk', 'PNG')
TILES_FOLDER = os.path.join(BASE_FOLDER, 'Tiles')
ITEMS_FOLDER = os.path.join(BASE_FOLDER, 'Items')
ENEMIES_FOLDER = os.path.join(BASE_FOLDER, 'Enemies')
HUD_FOLDER = os.path.join(BASE_FOLDER, 'HUD')

# Загрузка игрока (анимация ходьбы)
player_images = [load_image(PLAYER_FOLDER, f'p1_walk{i:02}.png') for i in range(1, 12)]
player_rect = player_images[0].get_rect(midbottom=(100, 500))
player_speed_y = 0
gravity = 1

# Загрузка плиток (окружение)
ground_tile = load_image(TILES_FOLDER, 'grassMid.png')
platform_tile = load_image(TILES_FOLDER, 'box.png')

# Загрузка предметов (монеты, шипы)
coin_image = load_image(ITEMS_FOLDER, 'coinGold.png')
spike_image = load_image(ITEMS_FOLDER, 'spikes.png')

# Загрузка врагов
enemy_image = load_image(ENEMIES_FOLDER, 'snailWalk1.png')

# Загрузка элементов интерфейса
heart_image = load_image(HUD_FOLDER, 'hud_heartFull.png')
coin_hud_image = load_image(HUD_FOLDER, 'hud_coins.png')

# Платформы на уровне
platforms = [pygame.Rect(100, 400, 100, 50), pygame.Rect(300, 300, 100, 50), pygame.Rect(500, 200, 100, 50)]

# Враги на уровне
enemies = [pygame.Rect(400, 500, 50, 50), pygame.Rect(600, 500, 50, 50)]

# Игровой цикл
running = True
clock = pygame.time.Clock()
frame = 0

while running:
    screen.fill((135, 206, 235))  # Голубой фон

    # Рендерим землю
    for x in range(0, WIDTH, ground_tile.get_width()):
        screen.blit(ground_tile, (x, 550))

    # Рендерим платформы
    for platform in platforms:
        screen.blit(platform_tile, platform)

    # Анимация игрока
    frame += 1
    player_image = player_images[frame % len(player_images)]
    screen.blit(player_image, player_rect)

    # Обработка гравитации
    player_speed_y += gravity
    player_rect.y += player_speed_y
    if player_rect.bottom >= 550:
        player_rect.bottom = 550
        player_speed_y = 0

    # Рендерим врагов
    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    # Рендерим предметы
    screen.blit(coin_image, (700, 500))
    screen.blit(spike_image, (500, 500))

    # Рендерим элементы интерфейса (жизни и монеты)
    screen.blit(heart_image, (20, 20))
    screen.blit(coin_hud_image, (60, 20))

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
    if keys[pygame.K_SPACE] and player_rect.bottom == 550:
        player_speed_y = -20

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
