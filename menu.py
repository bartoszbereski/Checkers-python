import pygame
import sys
import easygui
from button import Button
from checkers.constants import SQUARE_SIZE, WIDTH, HEIGHT
from checkers.game import Game
from checkers.board import Board
from minimax.algorithm import minimax
from checkers.constants import WHITE, RED
from network import Network
import threading

SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Menu")
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BG = pygame.image.load("assets/background1.png")
ai_on = False



def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def get_font(size):  # Returns Press-Start-2P in the desired size
    pygame.font.init()
    return pygame.font.Font("assets/font.ttf", size)


def main_menu():
    pygame.display.set_caption("MENU")
    while True:
        WIN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("MAIN MENU", True, "#ff80ed")   #b68f40
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250),
                             text_input="PLAY", font=get_font(50), base_color="#ffffff", hovering_color="Light Green")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 400),
                                text_input="OPTIONS", font=get_font(50), base_color="#ffffff",
                                hovering_color="Light Green")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 550),
                             text_input="QUIT", font=get_font(50), base_color="#ffffff", hovering_color="Light Green")

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.change_color(MENU_MOUSE_POS)
            button.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pygame.display.set_caption('Checkers')
                    pygame.display.set_mode((800, 800))
                    pygame.display.update()
                    play()
                if OPTIONS_BUTTON.check_for_input(MENU_MOUSE_POS):
                    options()

                if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def options():
    global ai_on
    ai_on = False
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        WIN.fill((137, 137, 137))
        OPTIONS_TEXT = get_font(45).render("Choose game type.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 100))
        WIN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        player_vs_player = Button(image=None, pos=(400, 200), text_input="PLAYER VS PLAYER", font=get_font(30), base_color="Black",
                                  hovering_color="Red")
        player_vs_ai = Button(image=None, pos=(400, 300), text_input="PLAYER VS AI    ", font=get_font(30), base_color="Black",
                              hovering_color="Red")
        OPTIONS_BACK = Button(image=None, pos=(400, 500), text_input="BACK", font=get_font(75), base_color="Black",
                              hovering_color="Green")
        for button in [player_vs_player, player_vs_ai, OPTIONS_BACK]:
            button.change_color(OPTIONS_MOUSE_POS)
            button.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_vs_player.check_for_input(OPTIONS_MOUSE_POS):
                    ai_on = False
                if player_vs_ai.check_for_input(OPTIONS_MOUSE_POS):
                    ai_on = True
                if OPTIONS_BACK.check_for_input(OPTIONS_MOUSE_POS):
                    main_menu()
        pygame.display.update()

n = Network()

def threaded_network_send(p):
    n.send(p)
    #print("Sending:", p)

def play():
    run = True
    clock = pygame.time.Clock()
    player_num = n.get_player_number()
    game = Game(WIN)
    board = Board()

    while run:
        p = n.get_p()
        clock.tick(FPS)
        if game.turn == WHITE and ai_on:
            value, new_board = minimax(game.get_board(), 4, WHITE, game)
            game.ai_move(new_board)
       # winner = game.winner()
       # if winner is not None:
            #message = f"{winner} wins!"
          #  easygui.msgbox(message, 'WINNER!')
            #run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                p1 = board.get_board()  # update p with the new board position
                print("before", p1)
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
                threading.Thread(target=threaded_network_send, args=(p1,)).start()
                if game.made_move():
                    pass
        game.update()
    pygame.quit()
