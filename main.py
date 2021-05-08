import pygame
import sys
import random
import numpy as np

pygame.init()


height_s = 52
width_s = 96
square_size = 20
width = width_s * square_size
height = (height_s * square_size) + 40
t = 50
text_margin = height - 40
win = pygame.display.set_mode((width, height))
running = False

pygame.display.set_caption("John Conway's Game of Life")

white = (225, 225, 225)
gray = (128, 128, 128)
black = (0, 0, 0)
grid = [[0 for i in range(height_s)] for i in range(width_s)]

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

    win.blit(text, (25, text_margin))

    while True:

        font = pygame.font.SysFont("arial", square_size * 2)
        text = font.render(f'Interval = {t} ms', False, gray)


        for event in pygame.event.get():

            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(win, black, pygame.Rect(375, text_margin, width, square_size * 2), 0)
            win.blit(font.render(f'Mouse = {((mouse_pos[1] / 100).__round__(1) * (width_s/(width/100))).__round__(1)}, {((mouse_pos[0] / 100).__round__(1) * (height_s/(height_s/5))).__round__(1)}', False, gray), (width - 375, text_margin))

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                vert = ((pos[0] / 100).__round__(1) * (height_s/(height_s/5))).__round__(1)
                hor = ((pos[1] / 100).__round__(1) * (width_s/(width/100))).__round__(1)

                try:
                    if hor < width_s or vert < height_s:
                        grid[int(vert)][int(hor)] = 1
                except IndexError:
                    pass

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                vert = ((pos[0] / 100).__round__(1) * (height_s/(height_s/5))).__round__(1)
                hor = ((pos[1] / 100).__round__(1) * (width_s/(width/100))).__round__(1)
                try:
                    if hor < width_s - 1 or vert < height_s - 1:
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
                        pygame.draw.rect(win, black, pygame.Rect(25, text_margin, width, square_size * 2), 0)
                        win.blit(font.render(f'Interval = {t} ms', False, gray), (25, text_margin))
                    elif t == 50:
                        t = 1
                        t = t.__round__(1)
                        pygame.draw.rect(win, black, pygame.Rect(25, text_margin, width, square_size * 2), 0)
                        win.blit(font.render(f'Interval = {t} ms', False, gray), (25, text_margin))

                elif event.key == pygame.K_LEFT:
                    if t != 1000:
                        if t == 1:
                            t = 50
                            t = t.__round__(1)
                            pygame.draw.rect(win, black, pygame.Rect(25, text_margin, width, square_size * 2), 0)
                            win.blit(font.render(f'Interval = {t} ms', False, gray), (25, text_margin))
                        else:
                            t += 50
                            t = t.__round__(1)
                            pygame.draw.rect(win, black, pygame.Rect(25, text_margin, width, square_size * 2), 0)
                            win.blit(font.render(f'Interval = {t} ms', False, gray), (25, text_margin))

                elif event.key == pygame.K_RETURN:
                    life()

                elif event.key == pygame.K_SPACE:
                    if running:
                        running = False
                    else:
                        running = True

                elif event.key == pygame.K_c:
                    grid = [[0 for x in range(height_s)] for y in range(width_s)]

                elif event.key == pygame.K_r:
                    grid = [[random.randint(0, 1) for x in range(height_s)] for y in range(width_s)]

                elif event.key == pygame.K_s:
                    pygame.draw.rect(win, black, pygame.Rect(25, text_margin, width, square_size * 2), 0)
                    win.blit(font.render('Input number 0-9 to save or ESC to cancel.', False, gray), (25, text_margin))
                    state_save = True
                    running = False

                elif state_save == True and int(event.key) in save_slots:
                    np.save(f'{event.key}.npy', np.array(grid))
                    pygame.draw.rect(win, black, pygame.Rect(25, text_margin, width, square_size * 2), 0)
                    win.blit(font.render(f'Interval = {t} ms', False, gray), (25, text_margin))
                    state_save = False

                elif event.key == pygame.K_l:
                    pygame.draw.rect(win, black, pygame.Rect(25, text_margin, width, square_size * 2), 0)
                    win.blit(font.render('Input number 0-9 to load or ESC to cancel.', False, gray), (25, text_margin))
                    state_load = True
                    running = False

                elif state_load == True and int(event.key) in save_slots:
                    grid = np.load(f'{event.key}.npy').tolist()
                    pygame.draw.rect(win, black, pygame.Rect(25, text_margin, width, square_size * 2), 0)
                    win.blit(font.render(f'Interval = {t} ms', False, gray), (25, text_margin))
                    state_load = False

                elif state_save == True:
                    if event.key == pygame.K_ESCAPE:
                        pygame.draw.rect(win, black, pygame.Rect(25, text_margin, width, square_size * 2), 0)
                        win.blit(font.render(f'Interval = {t} ms', False, gray), (25, text_margin))
                        state_save = False

                elif state_load == True:
                    if event.key == pygame.K_ESCAPE:
                        pygame.draw.rect(win, black, pygame.Rect(25, text_margin, width, square_size * 2), 0)
                        win.blit(font.render(f'Interval = {t} ms', False, gray), (25, text_margin))
                        state_load = False

                elif event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pygame.quit()
                    sys.exit()

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