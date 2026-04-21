import pygame
import copy
import time


def grid(state:list[list[int]], row:int, col:int, width:int, height:int) -> list:
    cell_width, cell_height = width/row, height/col
    grid_list = []
    for r in range(row):
        for c in range(col):
            cell = pygame.Rect(cell_width*c, cell_height*r, cell_width, cell_height)
            grid_list.append([cell, state[r][c]])
    return grid_list

def drawGrid(screen, grid_list:list) -> None:
    for cell in grid_list:
        match cell[1]:
            case 0:
                color = (90, 90, 90) # dark gray
            case 1:
                color = "white"
        pygame.draw.rect(screen, color, cell[0])
        pygame.draw.rect(screen, "gray", cell[0], 1)


def calculate(screen, state:list[list]) -> list[list]:
    row, col = len(state), len(state[0])
    next_gen = copy.deepcopy(state)

    def highlight(r, c, width, height):
        cell_width, cell_height = width/row, height/col
        cell = pygame.Rect(cell_width*c, cell_height*r, cell_width, cell_height)
        pygame.draw.rect(screen, "yellow", cell, 1)
        pygame.display.update()
        time.sleep(0.01)

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
                    # if state[r][c]:
                    #     highlight(r+i, c+j, 700, 700)

            if n < 2 or n > 3:
                next_gen[r][c] = 0
            elif n == 3:
                next_gen[r][c] = 1

    return next_gen


def main() -> int:
    width, height = 800, 800
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game of Life")

    row, col = int(height**0.5), int(width**0.5)
    state = [[0 for _ in range(col)] for _ in range(row)]
    grid_list = grid(state, row, col, width, height)

    running = False
    clock = pygame.time.Clock()
    while True:
        clock.tick(5)
        # print(clock.get_fps())
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
                    running = not running
                    state = calculate(screen, state)
                    grid_list = grid(state, row, col, width, height)
                if event.key == pygame.K_SPACE:
                    state = calculate(screen, state)
                    grid_list = grid(state, row, col, width, height)

        if running:
            state = calculate(screen, state)
            grid_list = grid(state, row, col, width, height)
        drawGrid(screen, grid_list)
        pygame.display.update()

if __name__=='__main__':
    main()