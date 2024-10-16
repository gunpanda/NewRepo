import pygame
from game import TetrisGame
from config import WIDTH, HEIGHT, BLOCK_SIZE

def get_player_name(screen):
    font = pygame.font.Font(None, 48)
    hint_surface = font.render('Ваше Имя:', True, (255, 255, 255))  # Подсказка
    input_box = pygame.Rect(WIDTH * BLOCK_SIZE // 4, HEIGHT * BLOCK_SIZE // 4 + 50, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    
    while True:
        screen.fill((0, 0, 0))  # Заливка черным цветом
        screen.blit(hint_surface, (WIDTH * BLOCK_SIZE // 4, HEIGHT * BLOCK_SIZE // 4))  # Отображаем подсказку
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text  # Возвращаем введенное имя
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE))
    pygame.display.set_caption("Tetris Game")
    
    player_name = get_player_name(screen)
    if player_name is None:
        return

    game = TetrisGame(screen, player_name)
    game.run()
    
    # Отображаем таблицу лидеров после завершения игры
    game.show_highscores()
    
    pygame.quit()

if __name__ == "__main__":
    main()
