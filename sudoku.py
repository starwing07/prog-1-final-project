import pygame
from board import Board

WIDTH = 600
HEIGHT = 700
BOARD_SZ = 540

bg = (255, 255, 255)
btn_color = (200, 200, 200)
btn_hover = (170, 170, 170)
txt_color = (0, 0, 0)


def draw_btn(screen, rect, text, font, mpos):
    if rect.collidepoint(mpos):
        c = btn_hover
    else:
        c = btn_color
    pygame.draw.rect(screen, c, rect, border_radius=8)
    lbl = font.render(text, True, txt_color)
    lbl_rect = lbl.get_rect(center=rect.center)
    screen.blit(lbl, lbl_rect)


def start_screen(screen, tfont, bfont, easy_r, med_r, hard_r):
    mpos = pygame.mouse.get_pos()
    screen.fill(bg)

    title = tfont.render("Sudoku", True, txt_color)
    sub = bfont.render("Select Difficulty", True, txt_color)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
    screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 220))

    draw_btn(screen, easy_r, "Easy", bfont, mpos)
    draw_btn(screen, med_r, "Medium", bfont, mpos)
    draw_btn(screen, hard_r, "Hard", bfont, mpos)


def game_screen(screen, brd, font, reset_r, restart_r, exit_r):
    mpos = pygame.mouse.get_pos()
    screen.fill(bg)

    if brd:  # make sure board exists
        brd.draw()

    draw_btn(screen, reset_r, "Reset", font, mpos)
    draw_btn(screen, restart_r, "Restart", font, mpos)
    draw_btn(screen, exit_r, "Exit", font, mpos)


def end_screen(screen, msg, tfont, bfont, restart_r, exit_r):
    mpos = pygame.mouse.get_pos()
    screen.fill(bg)

    title = tfont.render(msg, True, txt_color)
    sub = bfont.render("Choose an option below", True, txt_color)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
    screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 260))

    draw_btn(screen, restart_r, "Restart", bfont, mpos)
    draw_btn(screen, exit_r, "Exit", bfont, mpos)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")

    title_font = pygame.font.SysFont(None, 72)
    btn_font = pygame.font.SysFont(None, 40)
    sm_font = pygame.font.SysFont(None, 32)

    easy_rect = pygame.Rect(WIDTH // 2 - 100, 280, 200, 50)
    medium_rect = pygame.Rect(WIDTH // 2 - 100, 350, 200, 50)
    hard_rect = pygame.Rect(WIDTH // 2 - 100, 420, 200, 50)

    reset_rect = pygame.Rect(40, 620, 150, 50)
    restart_rect = pygame.Rect(225, 620, 150, 50)
    exit_rect = pygame.Rect(410, 620, 150, 50)

    running = True
    game_state = "start"
    board = None
    curr_row = 0
    curr_col = 0
    val = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "start":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if easy_rect.collidepoint(x, y):
                        board = Board(540, 540, screen, "easy")
                        curr_row, curr_col = 0, 0
                        board.select(curr_row, curr_col)
                        val = 0
                        game_state = "playing"
                    elif medium_rect.collidepoint(x, y):
                        board = Board(540, 540, screen, "medium")
                        curr_row, curr_col = 0, 0
                        board.select(curr_row, curr_col)
                        val = 0
                        game_state = "playing"
                    elif hard_rect.collidepoint(x, y):
                        board = Board(540, 540, screen, "hard")
                        curr_row, curr_col = 0, 0
                        board.select(curr_row, curr_col)
                        val = 0
                        game_state = "playing"

            elif game_state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    pos = board.click(x, y)
                    if pos:
                        curr_row, curr_col = pos
                        board.select(curr_row, curr_col)
                    elif reset_rect.collidepoint(x, y):
                        board.reset_to_original()
                        val = 0
                    elif restart_rect.collidepoint(x, y):
                        board = None
                        game_state = "start"
                    elif exit_rect.collidepoint(x, y):
                        running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and curr_row > 0:
                        curr_row -= 1
                        board.select(curr_row, curr_col)
                    elif event.key == pygame.K_DOWN and curr_row < 8:
                        curr_row += 1
                        board.select(curr_row, curr_col)
                    elif event.key == pygame.K_LEFT and curr_col > 0:
                        curr_col -= 1
                        board.select(curr_row, curr_col)
                    elif event.key == pygame.K_RIGHT and curr_col < 8:
                        curr_col += 1
                        board.select(curr_row, curr_col)

                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        board.clear()
                        val = 0

                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        val = event.key - pygame.K_0
                        board.sketch(val)

                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if val != 0:
                            board.place_number(val)
                            board.update_board()
                            if board.is_full():
                                if board.check_board():
                                    game_state = "win"
                                else:
                                    game_state = "lose"

            elif game_state == "win" or game_state == "lose":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if restart_rect.collidepoint(x, y):
                        board = None
                        game_state = "start"
                    elif exit_rect.collidepoint(x, y):
                        running = False

        if game_state == "start":
            start_screen(screen, title_font, btn_font, easy_rect, medium_rect, hard_rect)
        elif game_state == "playing":
            game_screen(screen, board, sm_font, reset_rect, restart_rect, exit_rect)
        elif game_state == "win":
            end_screen(screen, "You Win!", title_font, btn_font, restart_rect, exit_rect)
        elif game_state == "lose":
            end_screen(screen, "Game Over", title_font, btn_font, restart_rect, exit_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()