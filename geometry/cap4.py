import pygame
import random

# Константы
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1043
GROUND_Y = 680

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

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
        pygame.mixer.music.load("c:\\code\\geometry\\mu.mp3")
        pygame.mixer.music.play(-1)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.game_over:
                self.hero.jump()

    def update(self):
        if not self.game_over:
            self.hero.update()
            self.obstacle.update()
            self.coin.update()
            self.background.update(speed=10)

            # Проверка столкновения героя с препятствием
            if self.hero.get_collision_rect().colliderect(self.obstacle.get_collision_rect()):
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    self.obstacle = Obstacle(OBSTACLE_SPRITES, speed=10)
                    self.coin = Coin(COIN_SPRITES, speed=10, obstacle_rect=self.obstacle.rect)

            # Проверка на сбор монеты
            if self.hero.get_collision_rect().colliderect(self.coin.rect):
                self.score += 5
                self.coin = Coin(COIN_SPRITES, speed=10, obstacle_rect=self.obstacle.rect)

            # Если препятствие ушло за экран, создаём новое и увеличиваем очки
            if self.obstacle.off_screen():
                self.score += 1
                self.obstacle = Obstacle(OBSTACLE_SPRITES, speed=10)
                self.coin = Coin(COIN_SPRITES, speed=10, obstacle_rect=self.obstacle.rect)

    def draw(self, surface):
        self.background.draw(surface)
        self.obstacle.draw(surface)
        self.coin.draw(surface)
        self.hero.draw(surface)
        self.draw_text(surface, f'Score: {self.score}', 36, (255, 255, 255), 10, 10)
        self.draw_text(surface, f'Lives: {self.lives}', 36, (255, 255, 255), 10, 50)
        if self.game_over:
            self.draw_text(surface, 'Game Over', 100, (255, 0, 0), SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50)
            self.draw_text(surface, f'Score: {self.score}', 50, (255, 255, 255), SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50)

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
