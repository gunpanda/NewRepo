import pygame
import random
import os
import math

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
PURPLE = (128, 0, 128)

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
    pygame.mixer.music.play(-1)

hit_sound = pygame.mixer.Sound(hit_sound_path) if os.path.exists(hit_sound_path) else None
shoot_sound = pygame.mixer.Sound(shoot_sound_path) if os.path.exists(shoot_sound_path) else None
powerup_sound = pygame.mixer.Sound(powerup_sound_path) if os.path.exists(powerup_sound_path) else None

# Класс для частиц
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 4)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.lifetime = 30

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Класс для платформы
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 40
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = BLUE
        self.powerup_active = False
        self.powerup_timer = 0
    
    def move(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        # Добавляем свечение при активном призе
        if self.powerup_active:
            glow_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*self.color, 100), (10, 10, self.width, self.height))
            screen.blit(glow_surface, (self.rect.x - 10, self.rect.y - 10))

# Класс для мяча
class Ball:
    def __init__(self):
        self.radius = 10
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = random.choice([-5, 5])
        self.speed_y = -5
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.color = RED
        self.trail = []
        self.max_trail = 5
    
    def move(self):
        # Сохраняем предыдущую позицию для следа
        self.trail.append((self.rect.x + self.radius, self.rect.y + self.radius))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

    def draw(self):
        # Рисуем след мяча
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            trail_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (*self.color, alpha), (self.radius, self.radius), self.radius)
            screen.blit(trail_surface, (pos[0] - self.radius, pos[1] - self.radius))
        
        pygame.draw.circle(screen, self.color, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

# Класс для блоков
class Block:
    def __init__(self, x, y, width, height, health, block_type="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.max_health = health
        self.block_type = block_type
        self.color = self.get_color()
        self.particles = []

    def get_color(self):
        if self.block_type == "hard":
            return PURPLE
        elif self.health == 3:
            return RED
        elif self.health == 2:
            return ORANGE
        elif self.health == 1:
            return YELLOW
    
    def hit(self):
        self.health -= 1
        if self.health > 0:
            self.color = self.get_color()
            # Создаем частицы при ударе
            for _ in range(5):
                self.particles.append(Particle(
                    self.rect.centerx,
                    self.rect.centery,
                    self.color
                ))
        if hit_sound:
            hit_sound.play()

    def update_particles(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        for particle in self.particles:
            particle.draw()

# Класс для пуль
class Bullet:
    def __init__(self, x, y, bullet_type="normal"):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed_y = -10
        self.bullet_type = bullet_type
        self.color = WHITE if bullet_type == "normal" else YELLOW
        self.particles = []
    
    def move(self):
        self.rect.y += self.speed_y
        # Добавляем частицы для улучшенных пуль
        if self.bullet_type == "laser":
            self.particles.append(Particle(
                self.rect.centerx,
                self.rect.bottom,
                YELLOW
            ))
    
    def update_particles(self):
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        for particle in self.particles:
            particle.draw()

# Класс для призов
class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed_y = 5
        self.active = False
        self.effect = random.choice([
            "expand_paddle",
            "speed_ball",
            "extra_life",
            "laser",
            "multiball",
            "shield"
        ])
        self.color = self.get_color()
        self.particles = []

    def get_color(self):
        colors = {
            "expand_paddle": BLUE,
            "speed_ball": RED,
            "extra_life": GREEN,
            "laser": YELLOW,
            "multiball": PURPLE,
            "shield": ORANGE
        }
        return colors.get(self.effect, WHITE)

    def move(self):
        self.rect.y += self.speed_y
        # Добавляем частицы
        if random.random() < 0.3:
            self.particles.append(Particle(
                self.rect.centerx,
                self.rect.centery,
                self.color
            ))

    def update_particles(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        for particle in self.particles:
            particle.draw()

# Функция для создания сетки блоков
def create_blocks(rows, cols, level):
    blocks = []
    block_width = WIDTH // cols
    block_height = 30
    for row in range(rows):
        for col in range(cols):
            block_x = col * block_width
            block_y = row * block_height
            # Увеличиваем сложность с каждым уровнем
            if level > 3 and random.random() < 0.2:
                health = 4
                block_type = "hard"
            else:
                health = random.choice([1, 2, 3])
                block_type = "normal"
            block = Block(block_x, block_y, block_width, block_height, health, block_type)
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
level = 1
blocks = create_blocks(5, 8, level)
powerups = []
bullets = []
score = 0
lives = 3
game_state = "playing"  # playing, paused, game_over, victory

# Игровой цикл
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_state = "paused" if game_state == "playing" else "playing"
            elif event.key == pygame.K_r and game_state in ["game_over", "victory"]:
                # Перезапуск игры
                level = 1
                score = 0
                lives = 3
                blocks = create_blocks(5, 8, level)
                powerups = []
                bullets = []
                ball = Ball()
                paddle = Paddle()
                game_state = "playing"
    
    if game_state == "playing":
        # Управление платформой
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-paddle.speed)
        if keys[pygame.K_RIGHT]:
            paddle.move(paddle.speed)

        # Стрельба при нажатии пробела
        if keys[pygame.K_SPACE]:
            bullet_type = "laser" if paddle.powerup_active and paddle.powerup_timer > 0 else "normal"
            bullet = Bullet(paddle.rect.centerx, paddle.rect.top, bullet_type)
            bullets.append(bullet)
            if shoot_sound:
                shoot_sound.play()

        # Движение мяча
        ball.move()

        # Движение пуль
        for bullet in bullets[:]:
            bullet.move()
            bullet.update_particles()
            bullet.draw()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)
            for block in blocks[:]:
                if bullet.rect.colliderect(block.rect):
                    block.hit()
                    bullets.remove(bullet)
                    score += 10
                    if block.health == 0:
                        blocks.remove(block)
                        score += 50
                        powerup = create_powerup(block.rect.x, block.rect.y)
                        if powerup:
                            powerups.append(powerup)
                    break

        # Проверка столкновения мяча с платформой
        if ball.rect.colliderect(paddle.rect):
            # Улучшенная физика отскока
            relative_intersect_x = (paddle.rect.centerx - ball.rect.centerx) / (paddle.width / 2)
            ball.speed_x = -relative_intersect_x * 8
            ball.speed_y = -abs(ball.speed_y)
            ball.color = random.choice([RED, BLUE, GREEN, YELLOW, ORANGE])

        # Проверка столкновений с блоками
        for block in blocks[:]:
            if ball.rect.colliderect(block.rect):
                ball.speed_y = -ball.speed_y
                block.hit()
                if block.health == 0:
                    blocks.remove(block)
                    score += 50
                    powerup = create_powerup(block.rect.x, block.rect.y)
                    if powerup:
                        powerups.append(powerup)
            
        # Движение и проверка призов
        for powerup in powerups[:]:
            powerup.move()
            powerup.update_particles()
            powerup.draw()
            if powerup.rect.colliderect(paddle.rect):
                if powerup.effect == "expand_paddle":
                    paddle.width += 50
                    paddle.powerup_active = True
                    paddle.powerup_timer = 300
                elif powerup.effect == "speed_ball":
                    ball.speed_x *= 1.5
                    ball.speed_y *= 1.5
                elif powerup.effect == "extra_life":
                    lives += 1
                elif powerup.effect == "laser":
                    paddle.powerup_active = True
                    paddle.powerup_timer = 300
                elif powerup.effect == "multiball":
                    for _ in range(2):
                        new_ball = Ball()
                        new_ball.rect.x = ball.rect.x
                        new_ball.rect.y = ball.rect.y
                        new_ball.speed_x = random.choice([-5, 5])
                        new_ball.speed_y = -5
                        balls.append(new_ball)
                elif powerup.effect == "shield":
                    paddle.color = GREEN
                    paddle.powerup_active = True
                    paddle.powerup_timer = 300
                if powerup_sound:
                    powerup_sound.play()
                powerups.remove(powerup)

        # Обновление таймеров призов
        if paddle.powerup_active:
            paddle.powerup_timer -= 1
            if paddle.powerup_timer <= 0:
                paddle.powerup_active = False
                paddle.color = BLUE
                paddle.width = 100

        # Рисование объектов
        paddle.draw()
        ball.draw()
        for block in blocks:
            block.update_particles()
            block.draw()

        # Отображение счета, жизней и уровня
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счёт: {score}", True, WHITE)
        lives_text = font.render(f"Жизни: {lives}", True, WHITE)
        level_text = font.render(f"Уровень: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 120, 10))
        screen.blit(level_text, (WIDTH // 2 - 50, 10))

        # Проверка проигрыша
        if ball.rect.bottom >= HEIGHT:
            lives -= 1
            if lives == 0:
                game_state = "game_over"
            else:
                ball = Ball()

        # Проверка победы на уровне
        if not blocks:
            level += 1
            blocks = create_blocks(5, 8, level)
            ball = Ball()
            if level > 10:
                game_state = "victory"

    elif game_state == "paused":
        font = pygame.font.Font(None, 74)
        text = font.render("ПАУЗА", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, text_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Нажмите P для продолжения", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
        screen.blit(text, text_rect)

    elif game_state == "game_over":
        font = pygame.font.Font(None, 74)
        text = font.render("ИГРА ОКОНЧЕНА", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, text_rect)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Счёт: {score}", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
        screen.blit(text, text_rect)
        text = font.render("Нажмите R для перезапуска", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 + 100))
        screen.blit(text, text_rect)

    elif game_state == "victory":
        font = pygame.font.Font(None, 74)
        text = font.render("ПОБЕДА!", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, text_rect)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Счёт: {score}", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
        screen.blit(text, text_rect)
        text = font.render("Нажмите R для перезапуска", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 + 100))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
