import pygame
import sys
import random
import numpy as np

pygame.init()


amnt = 45
square_size = 20
width = amnt * square_size
height = width + 50
t = 50
win = pygame.display.set_mode((width, height))
running = False

pygame.display.set_caption("John Conway's Game of Life")

white = (225, 225, 225)
gray = (128, 128, 128)
black = (0, 0, 0)
grid = [[0 for i in range(amnt)] for i in range(amnt)]

arr = np.array(grid)

np.save('test2.npy', arr)
grid = np.load('test2.npy').tolist()
print(arr)
print(grid)


save_slots = [i for i in range(48, 58)]


def life():
    grid_copy = []
    for item in grid:
        grid_copy.append(item.copy())
    for x in range(1, len(grid) - 1):
        for y in range(1, len(grid[x]) - 1):
            borders = [grid_copy[x - 1][y - 1], grid_copy[x + 0][y - 1], grid_copy[x + 1][y - 1],
                       grid_copy[x - 1][y + 0],                          grid_copy[x + 1][y + 0],
                       grid_copy[x - 1][y + 1], grid_copy[x + 0][y + 1], grid_copy[x + 1][y + 1]]
            if grid[x][y] == 1:
                grid[x][y] = 0 if borders.count(1) < 2 else grid[x][y]
                grid[x][y] = 1 if borders.count(1) == 2 or borders.count(1) == 3 else grid[x][y]
                grid[x][y] = 0 if borders.count(1) > 3 else grid[x][y]
            else:
                grid[x][y] = 1 if borders.count(1) == 3 else grid[x][y]

def run():
    global running
    global t

    pygame.time.delay(t)
    life()

def main():
    global t
    global running
    global grid

    win.fill(black)

    font = pygame.font.SysFont("arial", square_size * 2)
    text = font.render(f'Interval = {t} ms', False, gray)

    state_save = False
    state_load = False

    win.blit(text, (25, height - 45))

    while True:

        font = pygame.font.SysFont("arial", square_size * 2)
        text = font.render(f'Interval = {t} ms', False, gray)


        for event in pygame.event.get():

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                vert = ((pos[0] / 100).__round__(1) * (amnt/(width/100))).__round__(1)
                hor = ((pos[1] / 100).__round__(1) * (amnt/(width/100))).__round__(1)
                try:
                    if hor < amnt or vert < amnt:
                        grid[int(vert)][int(hor)] = 1
                except IndexError:
                    pass

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                vert = ((pos[0] / 100).__round__(1) * (amnt/(width/100))).__round__(1)
                hor = ((pos[1] / 100).__round__(1) * (amnt/(width/100))).__round__(1)
                try:
                    if hor < amnt or vert < amnt:
                        grid[int(vert)][int(hor)] = 0
                except IndexError:
                    pass

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if t != 50:
                        t -= 50
                        t = t.__round__(1)
                        pygame.draw.rect(win, black, pygame.Rect(25, height - 45, width, square_size * 2), 0)
                        text = font.render(f'Interval = {t} ms', False, gray)
                        win.blit(text, (25, height - 45))
                        print(t)
                    else:
                        print(t)

                elif event.key == pygame.K_LEFT:
                    if t != 1000:
                        t += 50
                        t = t.__round__(1)
                        pygame.draw.rect(win, black, pygame.Rect(25, height - 45, width, square_size * 2), 0)
                        text = font.render(f'Interval = {t} ms', False, gray)
                        win.blit(text, (25, height - 45))
                        print(t)
                    else:
                        print(t)

                elif event.key == pygame.K_RETURN:
                    life()

                elif event.key == pygame.K_SPACE:
                    if running:
                        running = False
                    else:
                        running = True

                elif event.key == pygame.K_c:
                    grid = [[0 for i in range(amnt)] for i in range(amnt)]

                elif event.key == pygame.K_r:
                    grid = [[random.randint(0, 1) for i in range(amnt)] for i in range(amnt)]

                elif event.key == pygame.K_s:
                    pygame.draw.rect(win, black, pygame.Rect(25, height - 45, width, square_size * 2), 0)
                    win.blit(font.render('Input number 0-9 to save or ESC to cancel.', False, gray), (25, height - 45))
                    state_save = True
                    running = False

                elif state_save == True and int(event.key) in save_slots:
                    np.save(f'{event.key}.npy', np.array(grid))
                    pygame.draw.rect(win, black, pygame.Rect(25, height - 45, width, square_size * 2), 0)
                    text = font.render(f'Interval = {t} ms', False, gray)
                    win.blit(text, (25, height - 45))
                    state_save = False

                elif event.key == pygame.K_l:
                    pygame.draw.rect(win, black, pygame.Rect(25, height - 45, width, square_size * 2), 0)
                    win.blit(font.render('Input number 0-9 to load or ESC to cancel.', False, gray), (25, height - 45))
                    state_load = True
                    running = False

                elif state_load == True and int(event.key) in save_slots:
                    grid = np.load(f'{event.key}.npy').tolist()
                    pygame.draw.rect(win, black, pygame.Rect(25, height - 45, width, square_size * 2), 0)
                    text = font.render(f'Interval = {t} ms', False, gray)
                    win.blit(text, (25, height - 45))
                    state_load = False

                elif state_save == True:
                    if event.key == pygame.K_ESCAPE:
                        pygame.draw.rect(win, black, pygame.Rect(25, height - 45, width, square_size * 2), 0)
                        text = font.render(f'Interval = {t} ms', False, gray)
                        win.blit(text, (25, height - 45))
                        state_save = False

                elif state_load == True:
                    if event.key == pygame.K_ESCAPE:
                        pygame.draw.rect(win, black, pygame.Rect(25, height - 45, width, square_size * 2), 0)
                        text = font.render(f'Interval = {t} ms', False, gray)
                        win.blit(text, (25, height - 45))
                        state_load = False

        for x in range(0, len(grid)):
            for y in range(0, len(grid[x])):
                if grid[x][y] == 1:
                    pygame.draw.rect(win, white, pygame.Rect(x * square_size, y * square_size, square_size, square_size), 0)
                elif grid[x][y] == 0:
                    pygame.draw.rect(win, black, pygame.Rect(x * square_size, y * square_size, square_size, square_size),0)
                    pygame.draw.rect(win, gray, pygame.Rect(x * square_size, y * square_size, square_size, square_size), 1)


        pygame.display.update()

        if running:
            run()

main()