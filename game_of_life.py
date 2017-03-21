import sys
import random
import pygame

from colours import dark_blue, green, black

clock = pygame.time.Clock()


def draw_grid():
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, dark_blue, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, dark_blue, (0, y), (width, y))


def get_cells(density=0.2):
    cells = {}
    for c in range(columns):
        for r in range(rows):
            if random.random() < density:
                cells[c, r] = True
            else:
                cells[c, r] = False
    return cells


def draw_cells():
    for (x, y) in cells:
        colour = green if cells[x, y] else black
        rectangle = (x * cell_size, y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, colour, rectangle)


def get_neighbours((x, y)):
    positions = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y),
                 (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
    return [cells[r, c] for (r, c) in positions if 0 <= r < rows and 0 <= c < columns]


def evolve():
    global cells

    newCells = cells.copy()

    for position, alive in cells.items():
        live_neighbours = sum(get_neighbours(position))
        if alive:
            if live_neighbours not in [2, 3]:
                newCells[position] = False
        elif live_neighbours == 3:
            newCells[position] = True
    cells = newCells


pygame.init()
columns, rows = 50, 50
cell_size = 10
size = width, height = columns * cell_size, rows * cell_size
screen = pygame.display.set_mode(size)
cells = get_cells()

while True:

    clock.tick(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    draw_cells()
    evolve()
    draw_grid()
    pygame.display.update()