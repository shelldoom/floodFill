import pygame
from pygame import Surface
import pygame.gfxdraw
import pygame.constants
import pygame.locals
import sys
import random

size = resX, resY = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Flood Fill")
clock = pygame.time.Clock()

traversal_mode = "dfs"
cell_dimension = cell_width, cell_height = 20, 20
grid_dimension = rows, cols = resX // cell_width, resY // cell_height

grid = [[(255, 255, 255) for _ in range(cols)] for _ in range(rows)]

random_position = None
font = pygame.font.SysFont('bahnschrift', 20)


def display_grid(screen, grid, width=2, height=2) -> None:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            x, y = i * width, j * height
            cell_color = grid[i][j]
            pygame.draw.rect(
                screen,
                cell_color,
                pygame.Rect(x, y, width, height),
            )

def flood_fill(grid, start_pos, new_color=(150, 150, 0), traversal_mode="dfs"):
    old_color = grid[start_pos[0]][start_pos[1]]
    if old_color == new_color:
        return grid
    stack = [start_pos]
    removeIndex = -1 if traversal_mode == "dfs" else 0
    while len(stack) > 0:
        # Removes last item if traversal mode is dfs as if popping from a stack
        # pop(-1)   - DFS
        # Removes first item if traversal mode is bfs as if popping from front of the queue 
        # pop(0)    - BFS
        x, y = stack.pop(removeIndex)
        if grid[x][y] != old_color:
            continue
        grid[x][y] = new_color
        if x > 0:
            stack.append((x - 1, y))
        if y > 0:
            stack.append((x, y - 1))
        if x < len(grid) - 1:
            stack.append((x + 1, y))
        if y < len(grid[0]) - 1:
            stack.append((x, y + 1))
        yield grid

def pos_to_gridpos(pos):
    'Convert mouse coordinates to grid coordinates'
    row, col = pos[0] // cell_width, pos[1] // cell_height
    if row >= rows or col >= cols:
        return None, None
    return row, col

def color_cell(pos, color):
    'Color the cell indicated by the position of the mouse coordinate by the provided color'
    row, col = pos[0] // cell_width, pos[1] // cell_height
    if row >= rows or col >= cols:
        return
    grid[row][col] = color


grid_state_iterator = None
current_color = (210, 210, 210)

left_color = (0, 0, 0)
right_color = (255, 255, 255)
fill_color = (random.randrange(256), random.randrange(256), random.randrange(256))
text = font.render(f"Traversal Mode: {traversal_mode.upper()}     Fill Color:", False, (0, 0, 0))
color_buttonX, color_buttonY = text.get_width() + 10, 10
color_button_width, color_button_height = 50, 30

while 1:
    pygame.display.flip()
    clock.tick(FPS)
    screen.fill(0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                traversal_mode = "bfs" if traversal_mode.lower() == "dfs" else "dfs"

        if pygame.mouse.get_pressed()[0]:
            mouseX, mouseY = pygame.mouse.get_pos()
            if abs(mouseX-color_buttonX) <= color_button_width and abs(mouseY-color_buttonY) <= color_button_height:
                fill_color = (random.randrange(256), random.randrange(256), random.randrange(256))

            pos = pygame.mouse.get_pos()
            color_cell(pos, left_color)
        if pygame.mouse.get_pressed()[1] or pygame.key.get_pressed()[pygame.K_f]:
            pos = pygame.mouse.get_pos()
            pos = pos_to_gridpos(pos)
            grid_state_iterator = flood_fill(grid, pos, new_color=fill_color, traversal_mode=traversal_mode)
        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            color_cell(pos, right_color)

    if grid_state_iterator:
        try:
            grid = next(grid_state_iterator)
        except StopIteration:
            pass
    display_grid(screen, grid, *cell_dimension)
    text = font.render(f"Traversal Mode: {traversal_mode.upper()}     Fill Color:", False, (0, 0, 0))
    screen.blit(text, text.get_rect(topleft=(10, 10)))
    pygame.draw.rect(screen, fill_color, pygame.Rect(color_buttonX, color_buttonY, color_button_width, color_button_height))
