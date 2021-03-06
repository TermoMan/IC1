import pygame
import math
import random
from queue import PriorityQueue

cell_size = 25
rows = 20
columns = 20
height = cell_size * columns
width = cell_size * rows
win = pygame.display.set_mode((width + 200, height))


class Cell:
    def __init__(self, row, col, width = cell_size, color=(0, 0, 0), eyes=False):
        self.row = row
        self.col = col
        self.x = row * cell_size
        self.y = col * cell_size
        self.color = color
        self.neighbors = []
        self.width = width
        self.eyes = eyes

    def get_pos(self):
        return self.row, self.col

    def draw(self, surface):
        global rows, columns, width, height
        dis = width // rows
        i = self.row
        j = self.col
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))
        if self.eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

    def zeldas_disponibles(self, grid):

        self.neighbors = []

        if self.col < columns - 1 and self.row < rows - 1 and not grid[self.row + 1][self.col + 1].getColor() == (255, 0, 0):
            self.neighbors.append(grid[self.row + 1][self.col + 1])

        if self.row < rows - 1 and not grid[self.row + 1][self.col].getColor() == (255, 0, 0):
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.col < columns - 1 and self.row > 0 and not grid[self.row - 1][self.col + 1].getColor() == (255, 0, 0):
            self.neighbors.append(grid[self.row - 1][self.col + 1])

        if self.row > 0 and not grid[self.row - 1][self.col].getColor() == (255, 0, 0):
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col > 0 and self.row > 0 and not grid[self.row - 1][self.col - 1].getColor() == (255, 0, 0):
            self.neighbors.append(grid[self.row - 1][self.col - 1])

        if self.col < columns - 1 and not grid[self.row][self.col + 1].getColor() == (255, 0, 0):
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and self.row < rows - 1 and not grid[self.row + 1][self.col - 1].getColor() == (255, 0, 0):
            self.neighbors.append(grid[self.row + 1][self.col - 1])

        if self.col > 0 and not grid[self.row][self.col - 1].getColor() == (255, 0, 0):
            self.neighbors.append(grid[self.row][self.col - 1])

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color


def h(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)
    #return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - a[1]) ** 2)
    #return math.sqrt((a[1] - a[0]) ** 2 + (b[1] - b[0]) ** 2)



def aEstrella(draw, grid, start, end):
    count = 0
    open = PriorityQueue()
    open.put((0, count, start))
    came_from = {}
    g = {spot: float("inf") for row in grid for spot in row}
    g[start] = 0
    f = {spot: float("inf") for row in grid for spot in row}
    f[start] = h(start.get_pos(), end.get_pos())
    acum = 0
    openID = {start}

    while not open.empty():

        act = open.get()[2]
        openID.remove(act)

        if act == end:
            while end in came_from:
                acum += 1
                end = came_from[end]
                end.setColor((128, 0, 128))
                draw()
            return acum

        act.zeldas_disponibles(grid)

        for next in act.neighbors:
            if next.color != (128, 0, 128):
                next.setColor((255, 255, 0))
            temp_g = g[act] + 1

            if g[next] > temp_g:
                came_from[next] = act
                g[next] = temp_g
                f[next] = temp_g + h(next.get_pos(), end.get_pos())
                if next not in openID:
                    count += 1
                    open.put((f[next], count, next))
                    openID.add(next)

        draw()
    return -1


def create_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i, j, gap)
            grid[i].append(cell)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, (128, 128, 128), (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, (128, 128, 128), (j * gap, 0), (j * gap, width))


def redrawWindow(win, grid, rows, width):
    win.fill((0, 0, 0))

    for rw in grid:
        for cl in rw:
            cl.draw(win)

    start = pygame.Rect(width + 25, 25, 100, 25)
    quit = pygame.Rect(width + 25, 75, 100, 25)

    ori_btn = pygame.Rect(width + 25, 110, 100, 25)
    obj_btn = pygame.Rect(width + 25, 135, 100, 25)
    obs_btn = pygame.Rect(width + 25, 160, 100, 25)
    wp_btn = pygame.Rect(width + 25, 185, 100, 25)
    rst_btn = pygame.Rect(width + 25, 225, 100, 25)

    pygame.draw.rect(win, (200, 100, 100), start)
    win.blit(pygame.font.SysFont('calibri', 18).render("Empezar!", 1, (0, 0, 0)), (width + 30, 30))

    pygame.draw.rect(win, (0, 100, 200), quit)
    win.blit(pygame.font.SysFont('calibri', 20).render("Salir", 1, (0, 0, 0)), (width + 30, 80))

    pygame.draw.rect(win, (0, 200, 100), ori_btn)
    win.blit(pygame.font.SysFont('calibri', 20).render("Origin", 1, (0, 0, 0)), (width + 30, 115))

    pygame.draw.rect(win, (0, 0, 255), obj_btn)
    win.blit(pygame.font.SysFont('calibri', 20).render("Objetive", 1, (0, 0, 0)), (width + 30, 140))

    pygame.draw.rect(win, (255, 0, 0), obs_btn)
    win.blit(pygame.font.SysFont('calibri', 20).render("Obstacle", 1, (0, 0, 0)), (width + 30, 165))

    pygame.draw.rect(win, (255, 255, 255), wp_btn)
    win.blit(pygame.font.SysFont('calibri', 20).render("Way Point", 1, (0, 0, 0)), (width + 30, 190))

    pygame.draw.rect(win, (100, 200, 100), rst_btn)
    win.blit(pygame.font.SysFont('calibri', 20).render("Reset", 1, (0, 0, 0)), (width + 30, 230))

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    return y // gap, x // gap


def reset(grid, start, end):
    for rw in grid:
        for cl in rw:
            cl.setColor((0, 0, 0))

    or_x, or_y = randomPos(rows, columns)
    cell = grid[or_x][or_y]
    cell.setColor((0, 255, 0))
    cell.eyes = True
    start = cell
    start.row = or_x
    start.col = or_y
    ds_x, ds_y = randomPos(rows, columns)
    cell = grid[ds_x][ds_y]
    cell.setColor((0, 0, 255))
    end = cell
    end.pos = (ds_x, ds_y)




def randomPos(rows, columns):
    x = random.randrange(rows)
    y = random.randrange(columns)
    return x, y

def main(win, width):
    grid = create_grid(rows, width)
    pygame.init()

    or_x, or_y = randomPos(rows,columns)
    cell = grid[or_x][or_y]
    cell.setColor((0, 255, 0))
    cell.eyes = True
    start = cell
    ds_x, ds_y = randomPos(rows, columns)
    cell = grid[ds_x][ds_y]
    cell.setColor((0, 0, 255))
    end = cell

    wp_list = [start]
    sum = 0
    starts = pygame.Rect(width + 25, 25, 100, 25)
    quit = pygame.Rect(width + 25, 75, 100, 25)
    ori_btn = pygame.Rect(width + 25, 110, 100, 25)
    obj_btn = pygame.Rect(width + 25, 135, 100, 25)
    obs_btn = pygame.Rect(width + 25, 160, 100, 25)
    wp_btn = pygame.Rect(width + 25, 185, 100, 25)
    rst_btn = pygame.Rect(width + 25, 225, 100, 25)

    ori = True
    obj = False
    obs = False
    wp = False

    run = True
    while run:
        redrawWindow(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                if starts.collidepoint(pos):
                    print("Start")
                    wp_list.append(end)
                    for i in range(1 , len(wp_list)):
                        sum += aEstrella(lambda: redrawWindow(win, grid, rows, width), grid, wp_list[i-1], wp_list[i])
                    print("Ha recorrido: "+str(sum))

                elif quit.collidepoint(pos):
                    print("quit")
                    flag = False
                    pygame.quit()
                elif ori_btn.collidepoint(pos):
                    ori = True
                    obj = False
                    obs = False
                    wp = False
                elif obj_btn.collidepoint(pos):
                    ori = False
                    obj = True
                    obs = False
                    wp = False
                elif obs_btn.collidepoint(pos):
                    ori = False
                    obj = False
                    obs = True
                    wp = False
                elif wp_btn.collidepoint(pos):
                    ori = False
                    obj = False
                    obs = False
                    wp = True
                elif rst_btn.collidepoint(pos):
                    for rw in grid:
                        for cl in rw:
                            cl.setColor((0, 0, 0))

                    or_x, or_y = randomPos(rows, columns)
                    cell = grid[or_x][or_y]
                    cell.setColor((0, 255, 0))
                    cell.eyes = True
                    start = cell
                    start.row = or_x
                    start.col = or_y
                    ds_x, ds_y = randomPos(rows, columns)
                    cell = grid[ds_x][ds_y]
                    cell.setColor((0, 0, 255))
                    end = cell
                    end.pos = (ds_x, ds_y)
                    wp_list = [start]
                else:
                    row, col = get_clicked_pos(pos, rows, width)
                    if row < rows and col < columns:
                        cell = grid[row][col]
                        if ori:
                            cell.setColor((0, 255, 0))
                            cell.eyes = True
                            if start is not None:
                                start.eyer = False
                                start.setColor((0, 0, 0))
                            start = cell
                            wp_list[0] =start
                        elif obj:
                            cell.setColor((0, 0, 255))
                            if end is not None:
                                end.setColor((0, 0, 0))
                            end = cell
                        elif obs:
                            cell.setColor((255, 0, 0))
                        elif wp:
                            cell.setColor((255, 255, 255))
                            wp_list.append(cell)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    aEstrella(lambda: redrawWindow(win, grid, rows, width), grid, start, end)

    pygame.quit()


main(win, width)
