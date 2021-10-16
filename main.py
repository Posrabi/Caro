import time
import pygame

pygame.font.init()
pygame.init()

s_width = 750
s_height = 750
block_size = 50
available_spaces = (s_height / block_size) * (s_width/block_size)

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("TicTacToe")


class Player:
    def __init__(self, color, score=0):
        self.color = color
        self.score = score


def draw_text_middle(surface, text, size, color, position):
    """
    write text in the middle of the page
    :param position: x, y pos
    :param surface: window
    :param text:
    :param size:
    :param color:
    :return:
    """
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, position)


def create_grid():
    """
    create grid aka space
    :return: grid
    """
    grid = [[None for _ in range(int(s_height/block_size))] for _ in range(int(s_width/block_size))]
    return grid


def draw_grid(surface, grid):
    """
    draw lines separating the grid
    :param surface:
    :param grid:
    :return:
    """
    surface.fill((255, 255, 255))
    for i in range(len(grid)):
        pygame.draw.line(surface, (0, 0, 0), (0, i * block_size), (s_width, i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (0, 0, 0), (j*block_size, 0), (j*block_size, s_height))
    pygame.display.update()


def check_win(locked_pos, x, y, z_up, z_down, locked_pos_x):
    """
    check if player wins or not
    :param locked_pos_x: used pos for other player
    :param locked_pos: already used pos
    :param x: cur x
    :param y: cur y
    :param z_up: cur z_up
    :param z_down: cur z_down
    :return: bool
    """
    row = [(x, y, z_up, z_down)]  # initializes current value of x,y,z to lists
    col = [(x, y, z_up, z_down)]
    dia_up = [(x, y, z_up, z_down)]
    dia_down = [(x, y, z_up, z_down)]

    for element in locked_pos:
        if element[1] == y:
            row.append(element)
        if element[0] == x:
            col.append(element)
        if element[2] == z_up:
            dia_up.append(element)
        if element[3] == z_down:
            dia_down.append(element)

    row = sorted(row, key=lambda tup: tup[0])  # sort the lists according to the element that is different
    col = sorted(col, key=lambda tup: tup[1])
    dia_up = sorted(dia_up, key=lambda tup: tup[0])
    dia_down = sorted(dia_down, key=lambda tup: tup[1])

    for i in range(len(row) - 4): # iterate to find if there is 5 consecutive squares, if it is return true

        if row[i][0] + 50 == row[i+1][0] and row[i+1][0] + 50 == row[i+2][0] and row[i+2][0] + 50 == row[i+3][0] and \
                row[i+3][0] + 50 == row[i+4][0]:  # check if there is 5 consecutive squares

            if (row[i+4][0] + 50, row[i+4][1], row[i+4][2] + 50, row[i+4][3] + 50) in locked_pos_x and \
                    (row[i][0] - 50, row[i][1], row[i][2] - 50, row[i][3] - 50) in locked_pos_x:  # check if they are "sandwiched"

                return False

            return True

    for i in range(len(col) - 4):

        if col[i][1] + 50 == col[i+1][1] and col[i+1][1] + 50 == col[i+2][1] and col[i+2][1] + 50 == col[i+3][1] and \
                col[i+3][1] + 50 == col[i+4][1]:

            if (col[i + 4][0], col[i + 4][1] + 50, col[i + 4][2] + 50, col[i + 4][3] - 50) in locked_pos_x and \
                    (col[i][0], col[i][1] - 50, col[i][2] - 50, col[i][3] + 50) in locked_pos_x:

                return False

            return True
    for i in range(len(dia_up) - 4):

        if dia_up[i][0] + 50 == dia_up[i + 1][0] and dia_up[i + 1][0] + 50 == dia_up[i + 2][0] \
                and dia_up[i + 2][0] + 50 == dia_up[i + 3][0] and dia_up[i + 3][0] + 50 == dia_up[i + 4][0]:

            if (dia_up[i + 4][0] + 50, dia_up[i + 4][1]-50, dia_up[i + 4][2], dia_up[i + 4][3] + 100) in locked_pos_x and \
                    (dia_up[i][0] - 50, dia_up[i][1]+50, dia_up[i][2], dia_up[i][3] - 100) in locked_pos_x:

                return False

            return True

    for i in range(len(dia_down) - 4):

        if dia_down[i][1] + 50 == dia_down[i + 1][1] and dia_down[i + 1][1] + 50 == dia_down[i + 2][1] \
                and dia_down[i + 2][1] + 50 == dia_down[i + 3][1] and dia_down[i + 3][1] + 50 == dia_down[i + 4][1]:

            if (dia_down[i + 4][0] + 50, dia_down[i + 4][1] + 50, dia_down[i + 4][2]+100, dia_down[i + 4][3]) in locked_pos_x and \
                    (dia_down[i][0]-50, dia_down[i][1] - 50, dia_down[i][2] - 100, dia_down[i][3]) in locked_pos_x:

                return False

            return True

    return False


def main(circle, cross):

    turn_circle = True
    run = True
    locked_pos_cir = []
    locked_pos_cro = []
    grid = create_grid()
    draw_grid(win, grid)
    pygame.display.update()
    cross_pos = 10

    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x = (pygame.mouse.get_pos()[0] // block_size) * block_size  # round down the value of mouse pos to get the top left of the square
                y = (pygame.mouse.get_pos()[1] // block_size) * block_size
                z_up = x + y
                z_down = x - y

                if turn_circle:

                    if (x, y, z_up, z_down) not in locked_pos_cro and (x, y, z_up, z_down) not in locked_pos_cir:

                        pygame.draw.circle(win, circle.color, (x + (block_size/2), y + (block_size/2)), block_size/2.5, 5)
                        pygame.display.update()
                        turn_circle = False
                        if len(locked_pos_cir) >= 4:
                            if check_win(locked_pos_cir, x, y, z_up, z_down, locked_pos_cro):
                                run = False
                                circle.score += 1
                                time.sleep(0.5)
                                win.fill((255, 255, 255))
                                draw_text_middle(win, "Circle has won !!!", 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2 - 30))
                                draw_text_middle(win, "Circle scores: " + str(circle.score), 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2))
                                draw_text_middle(win, "Cross scores: " + str(cross.score), 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2 + 30))
                                pygame.display.update()
                                time.sleep(3)
                                win.fill((255, 255, 255))
                                pygame.display.update()

                        locked_pos_cir.append((x, y, z_up, z_down))

                else:

                    if (x, y, z_up, z_down) not in locked_pos_cir and (x, y, z_up, z_down) not in locked_pos_cro:
                        pygame.draw.line(win, cross.color, (x + cross_pos, y + cross_pos), (x + block_size - cross_pos, y + block_size - cross_pos), 5)
                        pygame.draw.line(win, cross.color, (x + block_size - cross_pos, y + cross_pos), (x + cross_pos, y + block_size - cross_pos), 5)
                        pygame.display.update()
                        turn_circle = True

                        if len(locked_pos_cro) >= 4:
                            if check_win(locked_pos_cro, x, y, z_up, z_down, locked_pos_cir):
                                run = False
                                cross.score += 1
                                time.sleep(0.5)
                                win.fill((255, 255, 255))
                                draw_text_middle(win, "Cross has won !!!", 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2 - 30))
                                draw_text_middle(win, "Circle scores: " + str(circle.score), 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2))
                                draw_text_middle(win, "Cross scores: " + str(cross.score), 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2 + 30))
                                pygame.display.update()
                                time.sleep(3)
                                win.fill((255, 255, 255))
                                pygame.display.update()

                        locked_pos_cro.append((x, y, z_up, z_down))
            # check for draw:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_r) or (event.type == pygame.MOUSEBUTTONDOWN and len(locked_pos_cir) + len(locked_pos_cro) >= available_spaces):
                run = False
                cross.score += 1
                circle.score += 1
                time.sleep(0.5)
                win.fill((255, 255, 255))
                draw_text_middle(win, "This round is a draw!!!", 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2 - 30))
                draw_text_middle(win, "Circle scores: " + str(circle.score), 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2))
                draw_text_middle(win, "Cross scores: " + str(cross.score), 20, (255, 0, 0), (s_width / 2 - 80, s_height / 2 + 30))
                pygame.display.update()
                time.sleep(3)
                win.fill((255, 255, 255))
                pygame.display.update()


def main_menu():
    circle = Player((0, 0, 0))
    cross = Player((255, 0, 0))
    run = True
    win.fill((0, 0, 0))
    draw_text_middle(win, "Press any button", 20, (255, 255, 255), (s_width / 2 - 80, s_height / 2 - 30))
    draw_text_middle(win, "(You can press r and declare any round draw if both got stuck)", 15, (255, 255, 255), (s_width / 2 - 230, s_height / 2))
    pygame.display.update()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(circle, cross)
                draw_text_middle(win, "Press any button to play again", 20, (0, 0, 0), (s_width / 2 - 145, s_height / 2 - 30))
                draw_text_middle(win, "(You can press r and declare any round draw if both got stuck)", 15, (0, 0, 0), (s_width / 2 - 230, s_height / 2))
                pygame.display.update()

    pygame.display.quit()


main_menu()  # run the program
