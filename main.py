#Snake Tutorial Python

import random
import pygame

class objetive(object):


    def __init__(self, start, color=(255, 0, 0)):
        self.pos = start
        self.color = color

    def move(self, pos):
        self.pos = pos

    def draw(self, surface):
        global rows, columns, width, height
        dis = width // rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

class obstacle(object):

    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def draw(self, surface):
        global rows, columns, width, height
        dis = width // rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))


class origin(object):

    def __init__(self, color, pos):
        self.color = color
        self.pos = pos



    def draw(self, surface, eyes = True):
        global rows, columns, width, height
        dis = width // rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

    def move (self, pos):
        self.pos = pos



def drawGrid(w, rows, columns ,surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
    for l in range(rows):
        x = x + sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))


    pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))
    for l in range(columns):
        y = y + sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))
    y = y + sizeBtwn
    pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))




def redrawWindow(surface):
    global rows, width, columns,  origin, objetive, list_obs, start, quit, ori_btn, obj_btn, obs_btn

    surface.fill((0, 0, 0))
    origin.draw(surface)
    objetive.draw(surface)
    for ob in list_obs:
        ob.draw(surface)

    pygame.draw.rect(surface, (200, 100, 100), start)
    surface.blit(pygame.font.SysFont('calibri', 18).render("Empezar!", 1, (0, 0, 0)), (width + 30, 30))

    pygame.draw.rect(surface, (0, 100, 200), quit)
    surface.blit(pygame.font.SysFont('calibri', 20).render("Salir", 1, (0, 0, 0)), (width + 30, 80))

    pygame.draw.rect(surface, (0, 200, 100), ori_btn)
    surface.blit(pygame.font.SysFont('calibri', 20).render("Origin", 1, (0, 0, 0)), (width + 30, 115))

    pygame.draw.rect(surface, (0, 100, 100), obj_btn)
    surface.blit(pygame.font.SysFont('calibri', 20).render("Objetive", 1, (0, 0, 0)), (width + 30, 140))

    pygame.draw.rect(surface, (100, 100, 100), obs_btn)
    surface.blit(pygame.font.SysFont('calibri', 20).render("Obstacle", 1, (0, 0, 0)), (width + 30, 165))


    drawGrid(width, rows, columns,  surface)
    pygame.display.update()


def randomPos(rows, columns):
    x = random.randrange(rows)
    y = random.randrange(columns)
    return x, y



def main():
    global width, height, rows, columns, origin, objetive, list_obs, play, start, quit, ori_btn, obj_btn, obs_btn

    cell_size = 25
    rows = 20
    columns = 10
    height = cell_size * columns
    width = cell_size * rows

    start = pygame.Rect(width + 25, 25, 75, 25)
    quit = pygame.Rect(width + 25, 75, 75, 25)
    list_obs = []

    ori_btn = pygame.Rect(width + 25, 110, 75, 25)
    obj_btn = pygame.Rect(width + 25, 135, 75, 25)
    obs_btn = pygame.Rect(width + 25, 160, 75, 25)

    origin = origin((0, 255, 0), randomPos(rows, columns))
    objetive = objetive(randomPos(rows, columns), color=(0, 0, 255))
    flag = True
    play = False

    ori = True
    obj = False
    obs = False

    pygame.init()
    win = pygame.display.set_mode((width + 200, height))

    clock = pygame.time.Clock()

    poss = [(1, 1), (1, 2), (1, 3)]

    while flag:
        pygame.time.delay(50)
        clock.tick(10)

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                flag = False
                pygame.quit()

            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = ev.pos
                if start.collidepoint(mouse_pos):
                    print("Start")
                    play = True

                elif quit.collidepoint(mouse_pos):
                    print("quit")
                    flag = False
                    pygame.quit()
                elif ori_btn.collidepoint(mouse_pos):
                    ori = True
                    obj = False
                    obs = False
                elif obj_btn.collidepoint(mouse_pos):
                    ori = False
                    obj = True
                    obs = False
                elif obs_btn.collidepoint(mouse_pos):
                    ori = False
                    obj = False
                    obs = True
                else:
                    print(mouse_pos[0] // cell_size, mouse_pos[1] // cell_size)
                    if ori:
                        origin.move((mouse_pos[0] // cell_size, mouse_pos[1] // cell_size))
                    elif obj:
                        objetive.move((mouse_pos[0] // cell_size, mouse_pos[1] // cell_size))
                    elif obs:
                        list_obs.append(obstacle((mouse_pos[0] // cell_size, mouse_pos[1] // cell_size), (255, 0, 0)))
        if play and poss:
            origin.move(poss.pop())
        if flag:
            redrawWindow(win)

    pass


main()