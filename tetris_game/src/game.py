import pygame
from tetris import Tetris

class TetrisGame:
    def __init__(self, screen, player_name):
        self.screen = screen
        self.player_name = player_name
        self.tetris = Tetris()
        self.clock = pygame.time.Clock()
        self.fall_speed = 40  # Базовая скорость падения в миллисекундах
        self.score = 0  # Счет игрока
        self.highscores = []  # Таблица лидеров

    def run(self):
        while True:
            dt = self.clock.tick(60)  # Устанавливаем FPS и получаем время в миллисекундах
            self.handle_events()  # Обработаем события
            self.update_game_state(dt)  # Обновим состояние игры с учетом времени
            self.render()  # Отобразим на экране

            if self.tetris.game_over:  # Если игра закончена, выходим из цикла
                break

        self.show_highscores()  # Отображаем таблицу лидеров после завершения игры

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.tetris.move(-1)  # Движение влево
                elif event.key == pygame.K_RIGHT:
                    self.tetris.move(1)  # Движение вправо
                elif event.key == pygame.K_DOWN:
                    self.fall_speed = 100  # Ускоренное падение
                elif event.key == pygame.K_UP:
                    self.tetris.rotate()  # Поворот фигуры

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.fall_speed = 500  # Сбросить скорость падения

    def update_game_state(self, dt):
        self.tetris.update(dt)  # Передаем время в метод обновления
        # Счет увеличивается за очищенные ряды
        if self.tetris.clear_rows():
            self.score += 100  # Добавить 100 очков за каждый очищенный ряд

    def render(self):
        self.screen.fill((0, 0, 0))  # Заливка черным цветом
        self.tetris.draw(self.screen)  # Отрисовка текущего состояния игры

        # Отображение счета
        font = pygame.font.Font(None, 36)
        score_surface = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))  # Счет в верхнем левом углу

        pygame.display.flip()  # Обновление экрана

    def show_highscores(self):
        self.highscores.append((self.player_name, self.score))  # Добавляем игрока и его счет
        self.highscores.sort(key=lambda x: x[1], reverse=True)  # Сортируем по убыванию счета

        # Отображение таблицы лидеров
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 48)
        title_surface = font.render("Таблица лидеров", True, (255, 255, 255))
        self.screen.blit(title_surface, (50, 50))

        for i, (name, score) in enumerate(self.highscores[:10]):  # Показываем топ-10
            entry_surface = font.render(f"{i + 1}. {name}: {score}", True, (255, 255, 255))
            self.screen.blit(entry_surface, (50, 100 + i * 50))

        pygame.display.flip()

        # Ожидаем завершения игры
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False  # Закрыть таблицу лидеров при нажатии Enter
