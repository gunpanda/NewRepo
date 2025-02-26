import pygame
import random
import os

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид с пулеметом")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Загрузка звуков
sound_path = os.path.join(os.path.dirname(__file__), 'arkanoid')
background_music_path = os.path.join(sound_path, 'background_music.mp3')
hit_sound_path = os.path.join(sound_path, 'hit.wav')
shoot_sound_path = os.path.join(sound_path, 'shoot.wav')
powerup_sound_path = os.path.join(sound_path, 'powerup.wav')

if os.path.exists(background_music_path):
    pygame.mixer.music.load(background_music_path)
    pygame.mixer.music.play(-1)  # Зацикливание музыки

hit_sound = pygame.mixer.Sound(hit_sound_path) if os.path.exists(hit_sound_path) else None
shoot_sound = pygame.mixer.Sound(shoot_sound_path) if os.path.exists(shoot_sound_path) else None
powerup_sound = pygame.mixer.Sound(powerup_sound_path) if os.path.exists(powerup_sound_path) else None

# Класс для платформы
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 40
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def move(self, dx):
        self.rect.x += dx
        # Не выходить за границы экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    
    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

# Класс для мяча
class Ball:
    def __init__(self):
        self.radius = 10
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = random.choice([-5, 5])
        self.speed_y = -5
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Отскок от стен
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

    def draw(self):
        pygame.draw.circle(screen, RED, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

# Класс для блоков
class Block:
    def __init__(self, x, y, width, height, health):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health  # Плотность (прочность) блока
        self.max_health = health
        self.color = self.get_color()

    def get_color(self):
        if self.health == 3:
            return RED
        elif self.health == 2:
            return ORANGE
        elif self.health == 1:
            return YELLOW
    
    def hit(self):
        self.health -= 1
        if self.health > 0:
            self.color = self.get_color()
        if hit_sound:
            hit_sound.play()

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Класс для пуль
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed_y = -10  # Скорость пули
    
    def move(self):
        self.rect.y += self.speed_y  # Пули двигаются вверх
    
    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Класс для призов
class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed_y = 5
        self.active = False
        self.effect = random.choice(["expand_paddle", "speed_ball", "extra_life"])

    def move(self):
        self.rect.y += self.speed_y

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

# Функция для создания сетки блоков
def create_blocks(rows, cols):
    blocks = []
    block_width = WIDTH // cols
    block_height = 30
    for row in range(rows):
        for col in range(cols):
            block_x = col * block_width
            block_y = row * block_height
            health = random.choice([1, 2, 3])  # Случайная прочность
            block = Block(block_x, block_y, block_width, block_height, health)
            blocks.append(block)
    return blocks

# Функция для создания призов
def create_powerup(x, y):
    if random.random() < 0.3:  # 30% шанс на появление приза
        return PowerUp(x, y)
    return None

# Создание объектов
paddle = Paddle()
ball = Ball()
blocks = create_blocks(5, 8)  # 5 рядов и 8 колонок блоков
powerups = []
bullets = []  # Список для пуль
score = 0
lives = 3

# Игровой цикл
running = True
while running:
    screen.fill(BLACK)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Управление платформой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move(-paddle.speed)
    if keys[pygame.K_RIGHT]:
        paddle.move(paddle.speed)

    # Стрельба при нажатии пробела
    if keys[pygame.K_SPACE]:
        # Пуля создается в центре платформы
        bullet = Bullet(paddle.rect.centerx, paddle.rect.top)
        bullets.append(bullet)
        if shoot_sound:
            shoot_sound.play()

    # Движение мяча
    ball.move()

    # Движение пуль
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw()
        # Удаление пули, если она выходит за пределы экрана
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
        # Проверка столкновения пули с блоками
        for block in blocks[:]:
            if bullet.rect.colliderect(block.rect):
                blocks.remove(block)
                bullets.remove(bullet)
                score += 10
                break

    # Проверка столкновения мяча с платформой
    if ball.rect.colliderect(paddle.rect):
        ball.speed_y = -ball.speed_y

    # Проверка столкновений с блоками
    for block in blocks[:]:
        if ball.rect.colliderect(block.rect):
            ball.speed_y = -ball.speed_y
            block.hit()
            if block.health == 0:
                blocks.remove(block)
                score += 50
                # Создание приза
                powerup = create_powerup(block.rect.x, block.rect.y)
                if powerup:
                    powerups.append(powerup)
             
    # Движение и проверка призов
    for powerup in powerups[:]:
        powerup.move()
        powerup.draw()
        if powerup.rect.colliderect(paddle.rect):
            if powerup.effect == "expand_paddle":
                paddle.width += 50  # Увеличение платформы
            elif powerup.effect == "speed_ball":
                ball.speed_x *= 1.5  # Ускорение мяча
                ball.speed_y *= 1.5
            elif powerup.effect == "extra_life":
                lives += 1  # Дополнительная жизнь
            if powerup_sound:
                powerup_sound.play()
            powerups.remove(powerup)  # Приз пойман, удаляем его
    
    # Рисование объектов
    paddle.draw()
    ball.draw()
    for block in blocks:
        block.draw()

    # Отображение счета и жизней
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))

    # Проверка проигрыша
    if ball.rect.bottom >= HEIGHT:
        lives -= 1
        if lives == 0:
            print("Game Over!")
            running = False
        else:
            ball = Ball()  # Перезапуск мяча

    # Проверка победы
    if not blocks:
        print("You Win!")
        running = False

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
