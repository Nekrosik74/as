
import pygame
import random

CELLSIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELLSIZE * COLS  # Added multiplication
HEIGHT = CELLSIZE * ROWS  # Fixed variable name and added multiplication
FPS = 60
FALLEVENT = pygame.USEREVENT + 1
FALLSPEED = 500  # ms

SHAPES = [  # Fixed list formatting
    [[1,1,1,1]],              # I
    [[1,1], [1,1]],           # O  # Fixed to 2D list
    [[0,1,0], [1,1,1]],       # T  # Fixed to 2D list
    [[1,1,0], [0,1,1]],       # Z  # Fixed to 2D list
    [[0,1,1], [1,1,0]],       # S  # Fixed to 2D list
    [[1,0,0], [1,1,1]],       # J  # Fixed to 2D list
    [[0,0,1], [1,1,1]],       # L  # Fixed to 2D list
]
COLORS = [  # Fixed list formatting
    (0,255,255), (255,255,0), (128,0,128),
    (255,0,0), (0,255,0), (0,0,255), (255,165,0),
]

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]  # Added missing bracket

class Piece:
    def __init__(self, x, y, idx):  # Fixed method name
        self.x = x
        self.y = y
        self.idx = idx
        self.shape = SHAPES[idx]
        self.color = COLORS[idx]
        
    def cells(self):
        for r, row in enumerate(self.shape):
            for c, val in enumerate(row):
                if val:
                    yield self.x + c, self.y + r
                    
    def rotate(self):
        self.shape = rotate(self.shape)

class Board:
    def __init__(self):
        self.grid = [[None] * COLS for _ in range(ROWS)]  # Fixed grid initialization
        
    def valid(self, piece, dx=0, dy=0):
        for x, y in piece.cells():
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= COLS or ny >= ROWS:
                return False
            if ny >= 0 and self.grid[ny][nx] is not None:
                return False
        return True
        
    def place(self, piece):
        for x, y in piece.cells():
            if 0 <= y < ROWS:
                self.grid[y][x] = piece.color
                
    def clear_lines(self):  # Fixed method name
        new = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = ROWS - len(new)
        for _ in range(cleared):
            new.insert(0, [None] * COLS)
        self.grid = new
        return cleared

def new_piece():  # Fixed function name
    idx = random.randrange(len(SHAPES))
    shape = SHAPES[idx]
    x = COLS // 2 - len(shape[0]) // 2
    return Piece(x, -len(shape), idx)

def draw_grid(s):  # Fixed function name
    for x in range(COLS):
        for y in range(ROWS):
            rect = pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE)  # Added multiplication
            pygame.draw.rect(s, (30, 30, 30), rect, 1)

def draw_board(s, board):  # Fixed function name
    for y, row in enumerate(board.grid):
        for x, col in enumerate(row):
            if col:
                r = pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE)  # Added multiplication
                pygame.draw.rect(s, col, r)
                pygame.draw.rect(s, (20, 20, 20), r, 2)

def draw_piece(s, piece):  # Fixed function name
    for x, y in piece.cells():
        if y >= 0:
            r = pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE)  # Added multiplication
            pygame.draw.rect(s, piece.color, r)
            pygame.draw.rect(s, (20, 20, 20), r, 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Fixed method name
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    board = Board()
    current = new_piece()  # Fixed function name
    pygame.time.set_timer(FALLEVENT, FALLSPEED)  # Fixed method name
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == FALLEVENT:
                if board.valid(current, dy=1):
                    current.y += 1
                else:
                    board.place(current)
                    lines = board.clear_lines()  # Fixed method name
                    score += lines * 100
                    current = new_piece()  # Fixed function name
                    if not board.valid(current):
                        running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and board.valid(current, dx=-1):  # Fixed constant name
                    current.x -= 1
                elif event.key == pygame.K_RIGHT and board.valid(current, dx=1):  # Fixed constant name
                    current.x += 1
                elif event.key == pygame.K_DOWN and board.valid(current, dy=1):
                    current.y += 1
                elif event.key == pygame.K_UP:
                    old = current.shape
                    current.rotate()
                    if not board.valid(current):
                        current.shape = old
                elif event.key == pygame.K_SPACE:
                    while board.valid(current, dy=1):
                        current.y += 1
                    board.place(current)
                    lines = board.clear_lines()  # Fixed method name
                    score += lines * 100
                    current = new_piece()  # Fixed function name
                    if not board.valid(current):
                        running = False

        screen.fill((0, 0, 0))
        draw_board(screen, board)  # Fixed function name
        draw_piece(screen, current)  # Fixed function name
        draw_grid(screen)  # Fixed function name
        
        font = pygame.font.SysFont(None, 24)
        img = font.render(f"Score {score}", True, (255, 255, 255))
        screen.blit(img, (5, 5))
        pygame.display.flip()
        clock.tick(FPS)

    font = pygame.font.SysFont(None, 48)
    img = font.render("Game Over", True, (255, 0, 0))
    screen.blit(img, (WIDTH // 2 - img.get_width() // 2, HEIGHT // 2 - img.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()

if __name__ == "__main__":
    main()