import pygame

# Инициализация Pygame
pygame.init()

# Загрузка спрайт-листа
sprite_sheet = pygame.image.load("c:\\code\\geometry\\sprite_sheet.png").convert_alpha()

# Определение размеров спрайтов
sprite_width = 64  # Ширина одного спрайта
sprite_height = 64  # Высота одного спрайта

# Извлечение спрайтов и их сохранение
def get_sprites_and_save(sheet, sprite_width, sprite_height):
    sprites = []
    for i in range(4):  # Предполагаем, что 4 спрайта
        x = i * sprite_width  # Положение по оси X
        sprite = sheet.subsurface(pygame.Rect(x, 0, sprite_width, sprite_height))
        sprites.append(sprite)

        # Сохранение спрайта как PNG-файл
        pygame.image.save(sprite, f"c:\\code\\geometry\\cap_sprite_{i + 1}.png")
        
    return sprites

# Получаем спрайты и сохраняем их
sprites = get_sprites_and_save(sprite_sheet, sprite_width, sprite_height)

# Пример: Отображение спрайтов (опционально)
screen = pygame.display.set_mode((256, 64))  # 4 спрайта по 64 пикселя в ширину
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Заполнение фона белым цветом

    # Отображение спрайтов
    for i, sprite in enumerate(sprites):
        screen.blit(sprite, (i * sprite_width, 0))

    pygame.display.flip()

pygame.quit()
