import pygame
from copy import deepcopy


class Board:
    # создание поля
    def __init__(self, width, height):
        self.field_color = pygame.Color('white')
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self):
        y = self.top
        for _ in range(self.height + 1):
            pygame.draw.line(screen, self.field_color, (self.left, y),
                             (self.left + self.cell_size * self.width, y))
            y += self.cell_size

        x = self.left
        for _ in range(self.width + 1):
            pygame.draw.line(screen, self.field_color, (x, self.top),
                             (x, self.top + self.cell_size * self.height))
            x += self.cell_size

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # cell - кортеж (x, y)
    def on_click(self, cell):
        x, y = cell
        color = self.board[y][x]
        for i in range(self.width):
            self.board[y][i] = color
        for i in range(self.height):
            self.board[i][x] = color

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        if cell_x < 0 or cell_x > self.width - 1 or cell_y < 0 or cell_y > self.height - 1:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)


class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2

    def render(self):
        super().render()
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]:
                    pygame.draw.rect(screen, pygame.Color('green'),
                                     (x * self.cell_size + self.left + 1,
                                      y * self.cell_size + self.top + 1,
                                      self.cell_size - 1,
                                      self.cell_size - 1))

    def next_move(self):
        board_copy = deepcopy(self.board)
        for line in range(self.height):
            for row in range(self.width):
                s = 0
                for y in range(-1, 2):
                    for x in range(-1, 2):
                        ly = line + y
                        rx = row + x
                        if row + x >= self.width or line + y >= self.height:
                            ly = ly % self.height
                            rx = rx % self.width
                        s += self.board[ly][rx]
                s -= self.board[line][row]
                if s == 3:
                    board_copy[line][row] = 1
                elif s < 2 or s > 3:
                    board_copy[line][row] = 0
        self.board = deepcopy(board_copy)


pygame.init()
size = 751, 751
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

board = Life(15, 15)
board.set_view(0, 0, 50)

v = 6
isLifeRunning = False

running = True

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.get_click(event.pos)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or \
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            isLifeRunning = not isLifeRunning
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            v += 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            v = max(0, v - 1)

    board.render()

    if isLifeRunning:
        board.next_move()
    pygame.display.flip()
    clock.tick(v)

pygame.quit()
