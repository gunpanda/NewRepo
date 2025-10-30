import pygame
import random
import os

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Определение параметров экрана
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Square Jump Game")

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)

# Загрузка спрайтов персонажа
hero_sprites = [
    pygame.transform.scale(pygame.image.load("cap_sprite_1.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("cap_sprite_2.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("cap_sprite_3.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("cap_sprite_4.png"), (80, 80))
]

# Загрузка спрайтов препятствий
obstacle_sprites = [
    pygame.transform.scale(pygame.image.load("obstacle_sprite1.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("obstacle_sprite2.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("obstacle_sprite3.png"), (50, 50))
]

# Загрузка спрайтов монет
coin_sprites = [
    pygame.transform.scale(pygame.image.load("coin_sprite1.png"), (30, 30)),
    pygame.transform.scale(pygame.image.load("coin_sprite2.png"), (30, 30)),
    pygame.transform.scale(pygame.image.load("coin_sprite3.png"), (30, 30))
]

# Загрузка фона
background = pygame.transform.scale(pygame.image.load("fon.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Настройки главного героя
hero_x = 100
hero_y = SCREEN_HEIGHT - 150
hero_speed = 5
jump_speed = 20
gravity = 1
hero_animation_speed = 0.2
current_hero_sprite = 0
hero_animation_timer = 0

# Настройки препятствий
obstacle_width = 50
max_obstacle_height = 250
obstacle_speed = 10
obstacles = []

# Настройки монет
coins = []
coin_speed = 10
coin_animation_speed = 0.15
current_coin_sprite = 0
coin_animation_timer = 0

# Настройки игры
score = 0
coins_collected = 0
lives = 3
font = pygame.font.Font(None, 74)
game_speed = 1.0

# Переменные для прыжка
is_jumping = False
jump_velocity = jump_speed

# Загрузка и воспроизведение музыки
pygame.mixer.music.load("mu.mp3")
pygame.mixer.music.play(-1)  # -1 означает бесконечное воспроизведение

def create_obstacle():
    obstacle_height = random.randint(50, max_obstacle_height)
    obstacle_y = SCREEN_HEIGHT - obstacle_height
    obstacle_type = random.randint(0, len(obstacle_sprites) - 1)
    return {
        'x': SCREEN_WIDTH,
        'y': obstacle_y,
        'height': obstacle_height,
        'type': obstacle_type
    }

def create_coin():
    return {
        'x': SCREEN_WIDTH,
        'y': random.randint(SCREEN_HEIGHT - 300, SCREEN_HEIGHT - 100)
    }

def game():
    global hero_y, is_jumping, jump_velocity, score, coins_collected, lives, game_speed
    global current_hero_sprite, hero_animation_timer, current_coin_sprite, coin_animation_timer

    obstacles.clear()
    coins.clear()
    obstacles.append(create_obstacle())
    coins.append(create_coin())

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not is_jumping:
                    is_jumping = True
                    jump_velocity = jump_speed

        # Анимация персонажа
        hero_animation_timer += hero_animation_speed
        if hero_animation_timer >= 1:
            hero_animation_timer = 0
            current_hero_sprite = (current_hero_sprite + 1) % len(hero_sprites)

        # Анимация монет
        coin_animation_timer += coin_animation_speed
        if coin_animation_timer >= 1:
            coin_animation_timer = 0
            current_coin_sprite = (current_coin_sprite + 1) % len(coin_sprites)

        # Движение героя и обработка прыжков
        if is_jumping:
            hero_y -= jump_velocity
            jump_velocity -= gravity
            if hero_y >= SCREEN_HEIGHT - 150:
                hero_y = SCREEN_HEIGHT - 150
                is_jumping = False

        # Движение препятствий
        for obstacle in obstacles[:]:
            obstacle['x'] -= obstacle_speed * game_speed
            if obstacle['x'] < -obstacle_width:
                obstacles.remove(obstacle)
                obstacles.append(create_obstacle())
                score += 1

        # Движение монет
        for coin in coins[:]:
            coin['x'] -= coin_speed * game_speed
            if coin['x'] < -30:
                coins.remove(coin)
                coins.append(create_coin())

        # Отображение главного героя
        screen.blit(hero_sprites[current_hero_sprite], (hero_x, hero_y))

        # Отображение препятствий
        for obstacle in obstacles:
            screen.blit(obstacle_sprites[obstacle['type']], 
                       (obstacle['x'], obstacle['y']))

        # Отображение монет
        for coin in coins:
            screen.blit(coin_sprites[current_coin_sprite], (coin['x'], coin['y']))

        # Проверка на столкновение с препятствиями
        for obstacle in obstacles:
            if (hero_x + hero_width > obstacle['x'] and 
                hero_x < obstacle['x'] + obstacle_width and
                hero_y + hero_height > obstacle['y']):
                lives -= 1
                if lives <= 0:
                    running = False
                else:
                    obstacles.remove(obstacle)
                    obstacles.append(create_obstacle())

        # Проверка сбора монет
        for coin in coins[:]:
            if (hero_x + hero_width > coin['x'] and 
                hero_x < coin['x'] + 30 and
                hero_y + hero_height > coin['y'] and 
                hero_y < coin['y'] + 30):
                coins.remove(coin)
                coins.append(create_coin())
                coins_collected += 1

        # Увеличение сложности
        game_speed = 1.0 + (score * 0.01)

        # Отображение счета и жизней
        score_text = font.render(f"Score: {score}", True, BLACK)
        coins_text = font.render(f"Coins: {coins_collected}", True, BLACK)
        lives_text = font.render(f"Lives: {lives}", True, BLACK)
        screen.blit(score_text, (50, 50))
        screen.blit(coins_text, (50, 120))
        screen.blit(lives_text, (50, 190))

        pygame.display.flip()
        clock.tick(60)

    # Отображение финального экрана
    screen.fill(LIGHT_GRAY)
    game_over_text = font.render("GAME OVER", True, BLACK)
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)
    final_coins_text = font.render(f"Coins Collected: {coins_collected}", True, BLACK)
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100))
    screen.blit(final_score_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2))
    screen.blit(final_coins_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 + 100))
    
    pygame.display.flip()
    pygame.time.wait(3000)

if __name__ == "__main__":
    game()
    pygame.quit()
