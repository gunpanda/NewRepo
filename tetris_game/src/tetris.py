import random
import pygame

# Определение форм тетромино
TETROMINOS = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]

class Tetris:
    def __init__(self):
        self.field = [[0 for _ in range(10)] for _ in range(20)]  # Игровое поле
        self.current_piece = None  # Текущая фигура
        self.next_piece = self.new_piece()  # Следующая фигура
        self.spawn_piece()  # Спавн первой фигуры
        self.game_over = False  # Флаг окончания игры
        
        self.fall_time = 0  # Время с последнего падения
        self.fall_speed = 500  # Скорость падения (в миллисекундах)

    def new_piece(self):
        return random.choice(TETROMINOS)

    def spawn_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        self.current_position = [0, 4]  # Начальная позиция

        # Проверка на наличие коллизий
        if self.check_collision(self.current_piece, self.current_position):
            self.game_over = True  # Игра окончена

    def check_collision(self, piece, position):
        for i, row in enumerate(piece):
            for j, cell in enumerate(row):
                if cell:
                    x = position[0] + i
                    y = position[1] + j
                    if (x < 0 or x >= len(self.field) or
                            y < 0 or y >= len(self.field[0]) or
                            self.field[x][y]):
                        return True
        return False

    def merge_piece(self):
        for i, row in enumerate(self.current_piece):
            for j, cell in enumerate(row):
                if cell:
                    x = self.current_position[0] + i
                    y = self.current_position[1] + j
                    self.field[x][y] = 1  # Ставим блок на поле

    def rotate(self):
        # Поворот фигуры
        rotated_piece = [list(row) for row in zip(*self.current_piece[::-1])]
        if not self.check_collision(rotated_piece, self.current_position):
            self.current_piece = rotated_piece

    def move(self, dx):
        # Перемещение фигуры
        new_position = [self.current_position[0], self.current_position[1] + dx]
        if not self.check_collision(self.current_piece, new_position):
            self.current_position = new_position

    def update(self, dt):
        # Обновление состояния игры
        if not self.game_over:
            self.fall_time += dt  # Увеличиваем время с последнего падения
            if self.fall_time >= self.fall_speed:  # Проверяем, если время истекло
                self.fall_time = 0  # Сбрасываем время
                self.current_position[0] += 1  # Падение фигуры
                if self.check_collision(self.current_piece, self.current_position):
                    self.current_position[0] -= 1  # Вернуться на одно место вверх
                    self.merge_piece()  # Зафиксировать фигуру
                    self.clear_rows()  # Удалить полные ряды
                    self.spawn_piece()  # Спавн следующей фигуры

    def draw(self, screen):
        # Отрисовка поля и фигур
        for i, row in enumerate(self.field):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, (255, 255, 255), (j * 30, i * 30, 30, 30), 0)  # Отрисовка блока

        # Отрисовка текущей фигуры
        for i, row in enumerate(self.current_piece):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, (255, 0, 0), ((self.current_position[1] + j) * 30, (self.current_position[0] + i) * 30, 30, 30), 0)

    def clear_rows(self):
        # Удаление полных рядов
        new_field = [row for row in self.field if any(cell == 0 for cell in row)]
        cleared_rows = len(self.field) - len(new_field)  # Количество очищенных рядов
        for _ in range(cleared_rows):
            new_field.insert(0, [0 for _ in range(10)])  # Добавляем пустые ряды сверху
        self.field = new_field  # Обновляем поле
        return cleared_rows  # Возвращаем количество очищенных рядов
