import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение параметров экрана
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Square Jump Game")

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)

# Загрузка главного героя
hero_image = pygame.image.load("c:\code\geometry\cap.png")
hero_width = 80
hero_height = 80
hero_image = pygame.transform.scale(hero_image, (hero_width, hero_height))

# Настройки главного героя (его начальные координаты и скорость)
hero_x = 100
hero_y = SCREEN_HEIGHT - 150
hero_speed = 5
jump_speed = 20
gravity = 1

# Настройки препятствий
obstacle_width = 50
max_obstacle_height = 250  # Максимальная высота препятствия, которую можно перепрыгнуть
obstacle_speed = 10
obstacle_color = (34, 139, 34)  # Цвет препятствий

# Настройки игры
score = 0
font = pygame.font.Font(None, 74)

# Переменные для прыжка
is_jumping = False
jump_velocity = jump_speed

# Главная функция игры
def game():
    global hero_y, is_jumping, jump_velocity, score, obstacle_height

    # Начальные параметры препятствия
    obstacle_x = SCREEN_WIDTH
    obstacle_height = random.randint(50, max_obstacle_height)
    obstacle_y = SCREEN_HEIGHT - obstacle_height

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(LIGHT_GRAY)  # Цвет фона

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Нажатие на пробел для прыжка
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not is_jumping:
                    is_jumping = True
                    jump_velocity = jump_speed

        # Движение героя и обработка прыжков
        if is_jumping:
            hero_y -= jump_velocity
            jump_velocity -= gravity
            if hero_y >= SCREEN_HEIGHT - 150:
                hero_y = SCREEN_HEIGHT - 150
                is_jumping = False

        # Движение препятствия
        obstacle_x -= obstacle_speed
        if obstacle_x < -obstacle_width:
            obstacle_x = SCREEN_WIDTH
            obstacle_height = random.randint(50, max_obstacle_height)  # Ограничиваем высоту препятствия
            obstacle_y = SCREEN_HEIGHT - obstacle_height
            score += 1

        # Отображение главного героя
        screen.blit(hero_image, (hero_x, hero_y))

        # Отображение препятствия
        pygame.draw.rect(screen, obstacle_color, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

        # Проверка на столкновение
        if hero_x + hero_width > obstacle_x and hero_x < obstacle_x + obstacle_width:
            if hero_y + hero_height > obstacle_y:
                running = False  # Завершаем игру при столкновении

        # Отображение счета
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (50, 50))

        pygame.display.flip()
        clock.tick(60)

# Запуск игры
if __name__ == "__main__":
    game()

pygame.quit()
