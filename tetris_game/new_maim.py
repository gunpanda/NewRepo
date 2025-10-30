import pygame
import random

# --- Константы ---
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300
PLAY_HEIGHT = 600
BLOCK_SIZE = 30
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH - 150) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50

# --- Фигуры ---
S_SHAPE = [[(0,0),(1,0),(-1,1),(0,1)], [(0,-1),(0,0),(1,0),(1,1)]]
Z_SHAPE = [[(-1,0),(0,0),(0,1),(1,1)], [(1,-1),(0,0),(1,0),(0,1)]]
I_SHAPE = [[(0,-1),(0,0),(0,1),(0,2)], [(-1,0),(0,0),(1,0),(2,0)]]
O_SHAPE = [[(0,0),(1,0),(0,1),(1,1)]]
T_SHAPE = [[(-1,0),(0,0),(1,0),(0,1)], [(0,-1),(-1,0),(0,0),(0,1)], [(-1,0),(0,0),(1,0),(0,-1)], [(0,-1),(1,0),(0,0),(0,1)]]
J_SHAPE = [[(-1,-1),(-1,0),(0,0),(1,0)], [(0,-1),(1,-1),(0,0),(0,1)], [(-1,0),(0,0),(1,0),(1,1)], [(0,-1),(0,0),(-1,1),(0,1)]]
L_SHAPE = [[(1,-1),(-1,0),(0,0),(1,0)], [(0,-1),(0,0),(0,1),(1,1)], [(-1,0),(0,0),(1,0),(-1,1)], [(-1,-1),(0,-1),(0,0),(0,1)]]
SHAPES = [S_SHAPE, Z_SHAPE, I_SHAPE, O_SHAPE, T_SHAPE, J_SHAPE, L_SHAPE]
SHAPE_COLORS = [(0,255,0),(255,0,0),(0,255,255),(255,255,0),(128,0,128),(0,0,255),(255,165,0)]

class Piece:
    def __init__(self, column, row, shape_idx):
        self.x, self.y = column, row
        self.shape_idx = shape_idx
        self.possible_rotations = SHAPES[shape_idx]
        self.color = SHAPE_COLORS[shape_idx]
        self.rotation = 0
    def get_formatted_shape(self): return self.possible_rotations[self.rotation % len(self.possible_rotations)]
    def get_shape_positions(self): return [(self.x + dx, self.y + dy) for dx, dy in self.get_formatted_shape()]
    def rotate(self, grid):
        original_rotation, original_x = self.rotation, self.x
        self.rotation = (self.rotation + 1) % len(self.possible_rotations)
        if not is_valid_space(self, grid):
            for dx_kick in [0, 1, -1, 2, -2]:
                self.x = original_x + dx_kick
                if is_valid_space(self, grid): return
                self.x = original_x
            self.rotation, self.x = original_rotation, original_x

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    for (c,r), color in locked_positions.items():
        if 0 <= r < 20 and 0 <= c < 10: grid[r][c] = color
    return grid

def get_new_piece(): return Piece(4, 0, random.randrange(len(SHAPES)))

def is_valid_space(piece, grid):
    for x, y in piece.get_shape_positions():
        if not (0 <= x < 10 and y < 20): return False # Check boundaries
        if y >= 0 and grid[y][x] != (0,0,0): return False # Check collision with locked pieces
    return True

def clear_rows(grid, locked_positions):
    full_rows = [r for r in range(19, -1, -1) if all(grid[r][c] != (0,0,0) for c in range(10))]
    if not full_rows: return 0
    cleared_count = len(full_rows)
    new_locked = {}
    # Sort by Y for correct shifting when multiple rows are cleared
    for (x,y), color in sorted(locked_positions.items(), key=lambda item: item[0][1]): 
        if y not in full_rows:
            shift = sum(1 for r_cleared in full_rows if r_cleared > y) # Count cleared rows below current block
            new_locked[(x, y + shift)] = color
    locked_positions.clear(); locked_positions.update(new_locked)
    return cleared_count

def draw_grid_lines(surface):
    for r_idx in range(21): pygame.draw.line(surface,(50,50,50),(TOP_LEFT_X,TOP_LEFT_Y+r_idx*BLOCK_SIZE),(TOP_LEFT_X+PLAY_WIDTH,TOP_LEFT_Y+r_idx*BLOCK_SIZE))
    for c_idx in range(11): pygame.draw.line(surface,(50,50,50),(TOP_LEFT_X+c_idx*BLOCK_SIZE,TOP_LEFT_Y),(TOP_LEFT_X+c_idx*BLOCK_SIZE,TOP_LEFT_Y+PLAY_HEIGHT))

def draw_window(surface, grid, score=0, level=0, lives=3, next_p=None, paused=False):
    surface.fill((20,20,30))
    font_title = pygame.font.SysFont('Consolas',50,bold=True); title_l=font_title.render('TETRIS',1,(200,200,255))
    surface.blit(title_l, (TOP_LEFT_X+PLAY_WIDTH+40,50))
    font_info = pygame.font.SysFont('Consolas',24); info_x_pos=TOP_LEFT_X+PLAY_WIDTH+25
    for i,txt_val in enumerate([f'Score: {score}',f'Level: {level}',f'Lives: {lives}']):
        surface.blit(font_info.render(txt_val,1,(255,255,255)),(info_x_pos,TOP_LEFT_Y+120+i*40))
    if next_p:
        next_l_render=font_info.render('Next:',1,(255,255,255)); surface.blit(next_l_render,(info_x_pos,TOP_LEFT_Y+240))
        current_shape=next_p.possible_rotations[0]; preview_bs=BLOCK_SIZE*0.6
        min_x_coord,max_x_coord=min(p[0] for p in current_shape),max(p[0] for p in current_shape)
        min_y_coord,max_y_coord=min(p[1] for p in current_shape),max(p[1] for p in current_shape)
        preview_w,preview_h=(max_x_coord-min_x_coord+1)*preview_bs,(max_y_coord-min_y_coord+1)*preview_bs
        offset_preview_x,offset_preview_y = info_x_pos+(100-preview_w)/2, TOP_LEFT_Y+270+(80-preview_h)/2 # Adjusted y for 'Next:'
        for dx_val,dy_val in current_shape:
            draw_x_coord,draw_y_coord = offset_preview_x+(dx_val-min_x_coord)*preview_bs, offset_preview_y+(dy_val-min_y_coord)*preview_bs
            pygame.draw.rect(surface,next_p.color,(draw_x_coord,draw_y_coord,preview_bs,preview_bs),0)
            pygame.draw.rect(surface,(128,128,128),(draw_x_coord,draw_y_coord,preview_bs,preview_bs),1)
    pygame.draw.rect(surface,(100,100,100),(TOP_LEFT_X-2,TOP_LEFT_Y-2,PLAY_WIDTH+4,PLAY_HEIGHT+4),4)
    draw_grid_lines(surface)
    for r_val,row_data in enumerate(grid):
        for c_val,color_data in enumerate(row_data):
            if color_data != (0,0,0):
                pygame.draw.rect(surface,color_data,(TOP_LEFT_X+c_val*BLOCK_SIZE,TOP_LEFT_Y+r_val*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE),0)
                pygame.draw.rect(surface,(50,50,50),(TOP_LEFT_X+c_val*BLOCK_SIZE,TOP_LEFT_Y+r_val*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE),1)
    if paused:
        pause_f=pygame.font.SysFont('Consolas',60,bold=True); pause_l=pause_f.render('PAUSED',1,(255,100,100))
        pause_s=pygame.Surface((PLAY_WIDTH,PLAY_HEIGHT//2),pygame.SRCALPHA); pause_s.fill((0,0,0,180))
        surface.blit(pause_s,(TOP_LEFT_X,TOP_LEFT_Y+PLAY_HEIGHT//4))
        surface.blit(pause_l,(TOP_LEFT_X+PLAY_WIDTH/2-pause_l.get_width()/2,TOP_LEFT_Y+PLAY_HEIGHT/2-pause_l.get_height()/2))
    pygame.display.update()

def draw_game_over_screen(surface, score):
    surface.fill((20,20,30))
    font_lrg=pygame.font.SysFont('Consolas',60,bold=True); font_sml=pygame.font.SysFont('Consolas',30)
    text_items=[('GAME OVER',font_lrg,(255,50,50),-120),(f'Final Score: {score}',font_sml,(255,255,255),-20),
           ('ANY KEY to Restart',font_sml,(200,200,255),50),('ESC to Quit',font_sml,(200,200,255),100)]
    for txt_content,font_obj,color_val,y_offset_val in text_items:
        label_obj=font_obj.render(txt_content,1,color_val); surface.blit(label_obj,(SCREEN_WIDTH/2-label_obj.get_width()/2,SCREEN_HEIGHT/2+y_offset_val))
    pygame.display.update()
    while True:
        for event_item in pygame.event.get():
            if event_item.type == pygame.QUIT: return False
            if event_item.type == pygame.KEYDOWN: return event_item.key != pygame.K_ESCAPE

def main(win):
    locked_positions = {}; current_piece, next_piece = get_new_piece(), get_new_piece()
    run_game, change_piece_flag, game_paused = True, False, False
    game_clock = pygame.time.Clock()
    fall_timer, current_score, current_level, total_lines_cleared, player_lives = 0,0,1,0,3
    initial_fall_speed, current_fall_speed = 0.40, 0.40

    while run_game:
        game_grid = create_grid(locked_positions)
        if total_lines_cleared >= current_level*10 and current_level < 15: 
            current_level+=1
            current_fall_speed=max(0.07,initial_fall_speed-(current_level-1)*0.025)
        
        if not game_paused: fall_timer += game_clock.get_rawtime()
        game_clock.tick(60) # Limit FPS

        if not game_paused and fall_timer/1000 >= current_fall_speed:
            fall_timer=0; current_piece.y+=1
            if not is_valid_space(current_piece,game_grid): current_piece.y-=1; change_piece_flag=True
        
        for event_obj in pygame.event.get():
            if event_obj.type == pygame.QUIT: run_game=False; pygame.quit(); quit()
            if event_obj.type == pygame.KEYDOWN:
                if event_obj.key == pygame.K_p: game_paused = not game_paused; fall_timer=0
                if not game_paused:
                    if event_obj.key == pygame.K_LEFT: 
                        current_piece.x-=1
                        if not is_valid_space(current_piece,game_grid): current_piece.x+=1
                    elif event_obj.key == pygame.K_RIGHT: 
                        current_piece.x+=1
                        if not is_valid_space(current_piece,game_grid): current_piece.x-=1
                    elif event_obj.key == pygame.K_DOWN: 
                        current_piece.y+=1
                        if not is_valid_space(current_piece,game_grid): current_piece.y-=1
                        else: current_score+=1
                    elif event_obj.key == pygame.K_UP: current_piece.rotate(game_grid)
                    elif event_obj.key == pygame.K_SPACE:
                        while is_valid_space(current_piece,game_grid): current_piece.y+=1; current_score+=2
                        current_piece.y-=1; change_piece_flag=True
        
        if game_paused: draw_window(win,game_grid,current_score,current_level,player_lives,next_piece,True); continue

        if change_piece_flag:
            for px_coord,py_coord in current_piece.get_shape_positions():
                if py_coord >= 0: locked_positions[(px_coord,py_coord)] = current_piece.color
            current_piece, next_piece = next_piece, get_new_piece(); change_piece_flag=False
            
            # Check Game Over condition: if new piece cannot be placed
            if not is_valid_space(current_piece, create_grid(locked_positions)): 
                player_lives -= 1
                if player_lives > 0:
                    locked_positions.clear() # Clear board for new life
                    current_piece, next_piece = get_new_piece(), get_new_piece() # Ensure new pieces are valid
                    current_fall_speed = max(0.07, initial_fall_speed - (current_level-1) * 0.025); fall_timer = 0
                else: # Final Game Over
                    if not draw_game_over_screen(win,current_score): run_game=False; break # Exit if user chooses to quit
                    # Reset game state for new game
                    locked_positions.clear(); current_score,current_level,total_lines_cleared,player_lives = 0,1,0,3
                    current_fall_speed,fall_timer = initial_fall_speed,0
                    current_piece,next_piece = get_new_piece(),get_new_piece()
                    if not run_game: break # Exit loop if draw_game_over_screen indicated quit
            
            grid_before_clear = create_grid(locked_positions) # Grid based on newly locked pieces
            cleared_rows_count = clear_rows(grid_before_clear,locked_positions) # locked_positions is updated in-place
            if cleared_rows_count > 0:
                total_lines_cleared+=cleared_rows_count
                score_points_map={1:40,2:100,3:300}; current_score+=score_points_map.get(cleared_rows_count,1200 if cleared_rows_count>=4 else 0)*current_level
        
        display_game_grid = create_grid(locked_positions) # Create grid with locked pieces
        # Draw current falling piece onto this display grid
        for x_coord,y_coord in current_piece.get_shape_positions():
            if 0<=y_coord<20 and 0<=x_coord<10: display_game_grid[y_coord][x_coord]=current_piece.color
        
        if run_game: draw_window(win,display_game_grid,current_score,current_level,player_lives,next_piece,game_paused)

def main_menu(win):
    title_font_obj=pygame.font.SysFont('Consolas',60,bold=True); option_font_obj=pygame.font.SysFont('Consolas',40)
    while True: # Main menu loop
        win.fill((20,20,30))
        title_label_obj=title_font_obj.render('Python Tetris',1,(200,200,255))
        start_label_obj=option_font_obj.render('Press any key to Start',1,(255,255,255))
        win.blit(title_label_obj,(SCREEN_WIDTH/2-title_label_obj.get_width()/2,SCREEN_HEIGHT/2-100))
        win.blit(start_label_obj,(SCREEN_WIDTH/2-start_label_obj.get_width()/2,SCREEN_HEIGHT/2+20))
        pygame.display.update()
        for event_main_menu in pygame.event.get():
            if event_main_menu.type == pygame.QUIT: pygame.quit(); quit()
            if event_main_menu.type == pygame.KEYDOWN: main(win); # Start game. Will return here after game over if not quit.

if __name__ == '__main__':
    pygame.init()
    pygame.font.init() # Initialize font module
    game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Python Tetris')
    main_menu(game_window)
