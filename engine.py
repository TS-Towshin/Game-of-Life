import pygame
import copy
import time

# Global Variables
width, height = 900, 900
row, col = int(height**0.5), int(width**0.5)

def grid(state:list[list[bool]], row:int,col:int, width:int, height:int) -> list[list[pygame.Rect, bool]]:
    '''
    Generate the grid
    '''

    cell_width, cell_height = width/row, height/col
    grid_list = []
    for r in range(row):
        for c in range(col):
            cell = pygame.Rect(cell_width*c, cell_height*r, cell_width, cell_height)
            grid_list.append([cell, state[r][c]])
    return grid_list

def highlight(screen, r: int, c: int) -> None:
    '''
    Highlight the surrounding area of an alive cell
    '''
    cell_width, cell_height = width/row, height/col
    pygame.draw.rect(screen, "yellow", (cell_width*c, cell_height*r, cell_width, cell_height), 1)
    pygame.display.update()   
#    time.sleep(0.01)

def drawGrid(screen, grid_list:list[list[pygame.Rect, bool]]) -> None:
    '''
    Draw the grid
    '''

    for cell in grid_list:
        color = (90, 90, 90) # dark gray
        if cell[1]:
            color = "white"
        pygame.draw.rect(screen, color, cell[0])
        pygame.draw.rect(screen, "gray", cell[0], 1)


def calculate(screen, state:list[list[bool]], hl: bool = False) -> list[list[bool]]:
    '''
    Calculate the next state of the game
    '''
    row, col = len(state), len(state[0])
    next_gen = copy.deepcopy(state)

    for r in range(row):
        for c in range(col):
            n = 0
            if r == 0 or r == row-1 or c == 0 or c == col-1:
                continue
            
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == j == 0:
                        continue
                    if state[r+i][c+j]:
                        n += 1
                    if state[r][c] and hl:
                        highlight(screen, r+i, c+j)

            if n < 2 or n > 3:
                next_gen[r][c] = 0
            elif n == 3:
                next_gen[r][c] = 1

    return next_gen


def main() -> int:
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game of Life")
    state = [[0 for _ in range(col)] for _ in range(row)]
    grid_list = grid(state, row, col, width, height)
    simulate = False
    hl = False
    clock = pygame.time.Clock()
    while True:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, cell in enumerate(grid_list):
                        if cell[0].collidepoint(event.pos):
                            r = i//row
                            c = i%col
                            state[r][c] = not state[r][c]
                            grid_list = grid(state, row, col, width, height)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = [[0 for _ in range(35)] for _ in range(35)]
                    grid_list = grid(state, row, col, width, height)
                if event.key == pygame.K_RETURN:
                    simulate = not simulate
                if event.key == pygame.K_SPACE:
                    state = calculate(screen, state, hl)
                    grid_list = grid(state, row, col, width, height)
                if event.key == pygame.K_h:
                    hl = not hl

        drawGrid(screen, grid_list)
        if simulate:
            state = calculate(screen, state, hl)
            grid_list = grid(state, row, col, width, height)

            simulate = False
            for rows in state:
                for cell in rows:
                    if cell:
                        simulate = True
        pygame.display.update()
if __name__=='__main__':
    main()
