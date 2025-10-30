import pygame
import random
import time
import os

# Константы
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1043
GROUND_Y = 680

# Инициализация Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Функция для безопасной загрузки звука
def load_sound(path):
    try:
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        else:
            # Создаем пустой звук как заглушку
            dummy_sound = pygame.mixer.Sound(buffer=b'')
            dummy_sound.set_volume(0)  # Отключаем звук
            return dummy_sound
    except:
        # В случае любой ошибки возвращаем заглушку
        dummy_sound = pygame.mixer.Sound(buffer=b'')
        dummy_sound.set_volume(0)
        return dummy_sound

# Загрузка звуковых эффектов
JUMP_SOUND = load_sound("c:\\code\\geometry\\jump.wav")
COIN_SOUND = load_sound("c:\\code\\geometry\\coin.wav")
HIT_SOUND = load_sound("c:\\code\\geometry\\hit.wav")
POWERUP_SOUND = load_sound("c:\\code\\geometry\\powerup.wav")

# Функция загрузки и масштабирования спрайтов
def load_sprite(path, size):
    sprite = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(sprite, size)

# Загрузка спрайтов препятствий
OBSTACLE_SPRITES = [
    load_sprite("c:\\code\\geometry\\obstacle_sprite1.png", (178, 196)),
    load_sprite("c:\\code\\geometry\\obstacle_sprite2.png", (178, 196)),
    load_sprite("c:\\code\\geometry\\obstacle_sprite3.png", (178, 196))
]

# Загрузка спрайтов героя
HERO_SPRITES = [
    load_sprite("c:\\code\\geometry\\cap_sprite_1.png", (128, 256)),
    load_sprite("c:\\code\\geometry\\cap_sprite_2.png", (128, 256)),
    load_sprite("c:\\code\\geometry\\cap_sprite_3.png", (128, 256)),
    load_sprite("c:\\code\\geometry\\cap_sprite_4.png", (128, 256))
]

# Загрузка спрайтов монет
COIN_SPRITES = [
    load_sprite("c:\\code\\geometry\\coin_sprite1.png", (50, 50)),
    load_sprite("c:\\code\\geometry\\coin_sprite2.png", (50, 50)),
    load_sprite("c:\\code\\geometry\\coin_sprite3.png", (50, 50))
]

# Загрузка фонового изображения
BACKGROUND_IMAGE = pygame.image.load("c:\\code\\geometry\\fon.png").convert()
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))


class Background:
    """Фон игры с эффектом параллакса."""
    def __init__(self, image, speed_factor=0.5):
        self.image = image
        self.speed_factor = speed_factor
        self.x1 = 0
        self.x2 = SCREEN_WIDTH

    def update(self, speed):
        self.x1 -= speed * self.speed_factor
        self.x2 -= speed * self.speed_factor
        if self.x1 <= -SCREEN_WIDTH:
            self.x1 = SCREEN_WIDTH
        if self.x2 <= -SCREEN_WIDTH:
            self.x2 = SCREEN_WIDTH

    def draw(self, surface):
        surface.blit(self.image, (self.x1, 0))
        surface.blit(self.image, (self.x2, 0))


class Hero:
    """Класс героя."""
    def __init__(self, sprites, x=100, y=GROUND_Y):
        self.sprites = sprites
        self.sprite_index = 0
        self.image = self.sprites[self.sprite_index]
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 128, 256)
        self.gravity = 0.5
        self.jump_speed = 15
        self.speed_y = 0
        self.is_jumping = False
        self.double_jump = False
        self.frame_counter = 0

    def update(self):
        # Анимация героя
        self.frame_counter += 1
        if self.frame_counter >= 10:
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            self.image = self.sprites[self.sprite_index]
            self.frame_counter = 0

        # Физика прыжка и гравитация
        if self.is_jumping:
            self.y += self.speed_y
            self.speed_y += self.gravity
            if self.y >= GROUND_Y:
                self.y = GROUND_Y
                self.is_jumping = False
                self.double_jump = False
                self.speed_y = 0

        self.rect.topleft = (self.x, self.y)

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.speed_y = -self.jump_speed
        elif not self.double_jump:
            self.double_jump = True
            self.speed_y = -self.jump_speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_collision_rect(self):
        # Немного уменьшаем зону столкновения для более точного определения столкновений
        return self.rect.inflate(-20, -20)


class Obstacle:
    """Класс препятствия."""
    def __init__(self, sprites, speed):
        self.sprites = sprites
        self.sprite_index = 0
        self.image = self.sprites[self.sprite_index]
        self.speed = speed
        self.width = 178
        self.height = random.randint(50, 150)
        self.x = SCREEN_WIDTH
        self.y = GROUND_Y - self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.frame_counter = 0

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x
        self.frame_counter += 1
        if self.frame_counter >= 10:
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            self.image = self.sprites[self.sprite_index]
            self.frame_counter = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def off_screen(self):
        return self.x < -self.width

    def get_collision_rect(self):
        return self.rect.inflate(-30, -30)


class Coin:
    """Класс монеты."""
    def __init__(self, sprites, speed, obstacle_rect):
        self.sprites = sprites
        self.sprite_index = 0
        self.image = self.sprites[self.sprite_index]
        self.speed = speed
        self.width = 50
        self.height = 50
        self.x, self.y = self.generate_position(obstacle_rect)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.frame_counter = 0

    def generate_position(self, obstacle_rect):
        # Генерация позиции монеты с проверкой на пересечение с препятствием
        while True:
            x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 400)
            y = random.randint(400, 650)
            coin_rect = pygame.Rect(x, y, self.width, self.height)
            if not coin_rect.colliderect(obstacle_rect):
                return x, y

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x
        self.frame_counter += 1
        if self.frame_counter >= 10:
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            self.image = self.sprites[self.sprite_index]
            self.frame_counter = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def off_screen(self):
        return self.x < -self.width


class PowerUp:
    """Класс бонуса."""
    def __init__(self, x, y, speed):
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 215, 0))  # Золотой цвет
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.type = random.choice(['shield', 'double_points', 'slow_time'])
        self.active = True

    def update(self):
        self.rect.x -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.right < 0


class Game:
    """Основной класс игры."""
    def __init__(self):
        self.hero = Hero(HERO_SPRITES)
        self.obstacle = Obstacle(OBSTACLE_SPRITES, speed=10)
        self.coin = Coin(COIN_SPRITES, speed=10, obstacle_rect=self.obstacle.rect)
        self.background = Background(BACKGROUND_IMAGE)
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.combo = 0
        self.combo_timer = 0
        self.powerups = []
        self.active_powerups = []
        self.start_time = time.time()
        self.game_speed = 10
        
        # Безопасная загрузка музыки
        try:
            if os.path.exists("c:\\code\\geometry\\mu.mp3"):
                pygame.mixer.music.load("c:\\code\\geometry\\mu.mp3")
                pygame.mixer.music.play(-1)
        except:
            pass  # Пропускаем загрузку музыки, если файл отсутствует или есть ошибка

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.game_over:
                self.hero.jump()
                JUMP_SOUND.play()

    def update(self):
        if not self.game_over:
            current_time = time.time()
            # Увеличение скорости игры со временем
            self.game_speed = 10 + (current_time - self.start_time) / 30
            self.hero.update()
            self.obstacle.update()
            self.coin.update()
            self.background.update(speed=self.game_speed)

            # Обновление комбо
            if current_time - self.combo_timer > 2:
                self.combo = 0

            # Обновление бонусов
            for powerup in self.powerups[:]:
                powerup.update()
                if powerup.off_screen():
                    self.powerups.remove(powerup)
                elif self.hero.get_collision_rect().colliderect(powerup.rect):
                    self.activate_powerup(powerup.type)
                    self.powerups.remove(powerup)
                    POWERUP_SOUND.play()

            # Проверка столкновения героя с препятствием
            if self.hero.get_collision_rect().colliderect(self.obstacle.get_collision_rect()):
                if 'shield' not in self.active_powerups:
                    self.lives -= 1
                    HIT_SOUND.play()
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self.reset_obstacle()
                else:
                    self.active_powerups.remove('shield')
                    self.reset_obstacle()

            # Проверка на сбор монеты
            if self.hero.get_collision_rect().colliderect(self.coin.rect):
                self.combo += 1
                self.combo_timer = current_time
                self.score += 5 * (1 + self.combo // 5)  # Бонус за комбо
                COIN_SOUND.play()
                self.coin = Coin(COIN_SPRITES, speed=self.game_speed, obstacle_rect=self.obstacle.rect)
                
                # Шанс появления бонуса
                if random.random() < 0.1:  # 10% шанс
                    self.powerups.append(PowerUp(SCREEN_WIDTH, random.randint(200, 600), self.game_speed))

            # Если препятствие ушло за экран
            if self.obstacle.off_screen():
                self.score += 1
                self.reset_obstacle()

    def reset_obstacle(self):
        self.obstacle = Obstacle(OBSTACLE_SPRITES, speed=self.game_speed)
        self.coin = Coin(COIN_SPRITES, speed=self.game_speed, obstacle_rect=self.obstacle.rect)

    def activate_powerup(self, powerup_type):
        self.active_powerups.append(powerup_type)
        if powerup_type == 'double_points':
            pygame.time.set_timer(pygame.USEREVENT, 10000)  # 10 секунд двойных очков
        elif powerup_type == 'slow_time':
            self.game_speed *= 0.5
            pygame.time.set_timer(pygame.USEREVENT + 1, 5000)  # 5 секунд замедления

    def draw(self, surface):
        self.background.draw(surface)
        self.obstacle.draw(surface)
        self.coin.draw(surface)
        for powerup in self.powerups:
            powerup.draw(surface)
        self.hero.draw(surface)
        
        # Отрисовка UI
        self.draw_text(surface, f'Score: {self.score}', 36, (255, 255, 255), 10, 10)
        self.draw_text(surface, f'Lives: {self.lives}', 36, (255, 255, 255), 10, 50)
        self.draw_text(surface, f'Combo: x{self.combo}', 36, (255, 255, 255), 10, 90)
        
        # Отрисовка активных бонусов
        y_offset = 130
        for powerup in self.active_powerups:
            self.draw_text(surface, f'Active: {powerup}', 24, (255, 215, 0), 10, y_offset)
            y_offset += 30

        if self.game_over:
            self.draw_text(surface, 'Game Over', 100, (255, 0, 0), SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50)
            self.draw_text(surface, f'Final Score: {self.score}', 50, (255, 255, 255), SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50)
            self.draw_text(surface, 'Press SPACE to restart', 36, (255, 255, 255), SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150)

    def draw_text(self, surface, text, size, color, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, (x, y))


def main():
    game = Game()
    running = True

    while running:
        clock.tick(60)  # Ограничение до 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_events(event)

        game.update()
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
