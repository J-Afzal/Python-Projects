import os
import sys
import time
import math
import random
import pygame
import chess


class Chess:
    def __init__(self):
        pygame.init()

        # Constants
        self.WINDOW_SIZE = 640
        self.PIECE_SIZE = 88
        self.SQUARE_SIZE = int(self.WINDOW_SIZE / 8)
        self.PIECE_PAD = int((self.SQUARE_SIZE - self.PIECE_SIZE) / 2)

        self.GAME_OVER_WIDTH = 350
        self.GAME_OVER_HEIGHT = 250

        self.WINDOW_BG_DARK = (81, 42, 42)
        self.WINDOW_BG_LIGHT = (124, 76, 62)
        self.MENU_WINDOW_BG = (8, 8, 8)
        self.PAWN_PROMOTION_BG = (162, 84, 84)

        self.SELECTED_PIECE_COLOUR = (192, 192, 75)
        self.PREVIOUS_MOVE_FROM_COLOUR = (128, 128, 50)
        self.PREVIOUS_MOVE_TO_COLOUR = (192, 192, 75)

        self.KING_IN_CHECK_COLOUR = (247, 119, 105)

        self.LEGAL_MOVE_COLOUR = (255, 255, 255, 100)
        self.LEGAL_MOVE_CAPTURE_COLOUR = (255, 0, 0, 100)
        self.LEGAL_MOVE_RADIUS = 12
        self.LEGAL_MOVE_CAPTURE_RADIUS = self.SQUARE_SIZE / 2
        self.LEGAL_MOVE_CAPTURE_WIDTH = 8

        self.TEXT_COLOUR = (255, 255, 255)
        self.SELECTED_TEXT_COLOUR = (0, 156, 128)

        self.FONT = 'Video Game Font'
        self.MAIN_MENU_TITLE_FONT = pygame.font.SysFont(self.FONT, 120)
        self.SUB_MENU_TITLE_FONT = pygame.font.SysFont(self.FONT, 90)
        self.MENU_OPTIONS_FONT = pygame.font.SysFont(self.FONT, 48)

        self.INFO_MENU_TITLE_FONT = pygame.font.SysFont(self.FONT, 90)
        self.INFO_MENU_BODY_FONT = pygame.font.SysFont(self.FONT, 28)
        self.INFO_MENU_RETURN_FONT = pygame.font.SysFont(self.FONT, 48)

        self.GAME_OVER_TITLE_FONT = pygame.font.SysFont(self.FONT, 48)
        self.GAME_OVER_OUTCOME_FONT = pygame.font.SysFont(self.FONT, 20)
        self.GAME_OVER_SCORE_FONT = pygame.font.SysFont(self.FONT, 72)

        # Variables
        pygame.display.set_caption('Chess')
        pygame.display.set_icon(pygame.image.load(self.get_path('app.ico')))
        self.window = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))

        self.number_of_players = 1
        self.ai_sleep_duration = 1

        self.human_player = chess.WHITE
        self.chess_board = None
        self.white_score = None
        self.black_score = None

        self.selected_piece = None
        self.selected_piece_grid_pos = None
        self.previous_move_piece = None
        self.previous_moves_from = None
        self.previous_moves_to = None
        self.new_grid_pos = None

        self.current_turn_is_AI = None
        self.go_to_main_menu = True
        self.game_is_over = None
        self.current_score = None

        self.mouse_button_down = None
        self.previous_mouse_position = (0, 0)

        self.menu_selection_sound = pygame.mixer.Sound(self.get_path('menu selection.wav'))
        self.start_sound = pygame.mixer.Sound(self.get_path('start.wav'))
        self.move_sound = pygame.mixer.Sound(self.get_path('move.wav'))
        self.castling_sound = pygame.mixer.Sound(self.get_path('castling.wav'))
        self.capture_sound = pygame.mixer.Sound(self.get_path('capture.wav'))
        self.check_sound = pygame.mixer.Sound(self.get_path('check.wav'))
        self.game_over_sound = pygame.mixer.Sound(self.get_path('game over.wav'))

        self.piece_pngs = {
            'K': pygame.transform.smoothscale(pygame.image.load(self.get_path('white king.png')), (self.PIECE_SIZE, self.PIECE_SIZE)),
            'Q': pygame.transform.smoothscale(pygame.image.load(self.get_path('white queen.png')), (self.PIECE_SIZE, self.PIECE_SIZE)),
            'B': pygame.transform.smoothscale(pygame.image.load(self.get_path('white bishop.png')), (self.PIECE_SIZE, self.PIECE_SIZE)),
            'R': pygame.transform.smoothscale(pygame.image.load(self.get_path('white rook.png')), (self.PIECE_SIZE, self.PIECE_SIZE)),
            'N': pygame.transform.smoothscale(pygame.image.load(self.get_path('white knight.png')), (self.PIECE_SIZE, self.PIECE_SIZE)),
            'P': pygame.transform.smoothscale(pygame.image.load(self.get_path('white pawn.png')), (self.PIECE_SIZE, self.PIECE_SIZE)),
            'k': pygame.transform.smoothscale(pygame.image.load(self.get_path('black king.png')), (self.PIECE_SIZE, self.PIECE_SIZE)),
            'q': pygame.transform.smoothscale(pygame.image.load(self.get_path('black queen.png')), (self.PIECE_SIZE, self.PIECE_SIZE)),
            'b': pygame.transform.smoothscale(pygame.image.load(self.get_path('black bishop.png')), (self.PIECE_SIZE, self.PIECE_SIZE)),
            'r': pygame.transform.smoothscale(pygame.image.load(self.get_path('black rook.png')), (self.PIECE_SIZE, self.PIECE_SIZE)),
            'n': pygame.transform.smoothscale(pygame.image.load(self.get_path('black knight.png')), (self.PIECE_SIZE, self.PIECE_SIZE)),
            'p': pygame.transform.smoothscale(pygame.image.load(self.get_path('black pawn.png')), (self.PIECE_SIZE, self.PIECE_SIZE)),
        }

        self.game_outcomes = [
            self.GAME_OVER_OUTCOME_FONT.render('(WHITE WINS)', True, self.TEXT_COLOUR),
            self.GAME_OVER_OUTCOME_FONT.render('(BLACK WINS)', True, self.TEXT_COLOUR),
            self.GAME_OVER_OUTCOME_FONT.render('(DRAW DUE TO STALEMATE)', True, self.TEXT_COLOUR),
            self.GAME_OVER_OUTCOME_FONT.render('(DRAW DUE TO INSUFFICIENT MATERIAL)', True, self.TEXT_COLOUR),
            self.GAME_OVER_OUTCOME_FONT.render('(DRAW DUE TO SEVENTY FIVE MOVES RULE)', True, self.TEXT_COLOUR),
            self.GAME_OVER_OUTCOME_FONT.render('(DRAW DUE TO FIVEFOLD REPETITION RULE)', True, self.TEXT_COLOUR),
            self.GAME_OVER_OUTCOME_FONT.render('(DRAW DUE TO FIFTY MOVES RULE)', True, self.TEXT_COLOUR),
            self.GAME_OVER_OUTCOME_FONT.render('(DRAW DUE TO THREEFOLD REPETITION RULE)', True, self.TEXT_COLOUR),
        ]

        self.blank_board = self.create_blank_board()
        self.main_menu_menus = self.create_menus(['PLAY CHESS', ' NO. OF PLAYERS', ' AI SPEED', ' INFO', ' QUIT'], 50, 50, 150, 100, self.MAIN_MENU_TITLE_FONT, self.MENU_OPTIONS_FONT, 0, 4)
        self.number_of_players_menus = self.create_menus(['NO. OF PLAYERS', ' 0', ' 1', ' 2', ' BACK TO MAIN MENU'], 50, 50, 150, 100, self.SUB_MENU_TITLE_FONT, self.MENU_OPTIONS_FONT, 1, 4)
        self.ai_speed_menus = self.create_menus(['AI SPEED', ' 0', ' 1', ' 2', ' BACK TO MAIN MENU'], 50, 50, 150, 100, self.SUB_MENU_TITLE_FONT, self.MENU_OPTIONS_FONT, 1, 4)
        self.info_menus = self.create_info_menu()
        self.game_over_menus = self.create_game_over_menu()

        # Game Loop
        self.game_loop()

    def game_loop(self):
        while True:
            if self.go_to_main_menu:
                self.display_main_menu()

            self.setup_game()

            while self.chess_board.outcome() is None and not self.go_to_main_menu:
                self.display_board()

                if self.is_next_turn_user():
                    self.get_next_move_from_user()
                else:
                    self.get_next_move_from_ai()

                self.display_board()

            if not self.go_to_main_menu:
                self.go_to_main_menu = self.display_game_over_menu()
                self.game_is_over = False

    def get_path(self, file_name):
        try:
            return os.path.join(sys._MEIPASS, file_name)
        except AttributeError:
            return 'chess\\resources\\' + file_name

    def setup_game(self):
        self.start_sound.play()

        self.mouse_button_down = False
        self.selected_piece_grid_pos = None
        self.selected_piece = None

        self.previous_moves_from = []
        self.previous_moves_to = []
        self.previous_move_piece = None

        self.chess_board = chess.Board()
        self.go_to_main_menu = False

    def is_next_turn_user(self):
        if self.number_of_players == 2:
            return True
        elif self.number_of_players == 1:
            if self.chess_board.turn == self.human_player:
                return True
            else:
                return False
        else:  # == 0:
            return False

    def display_main_menu(self):
        current_selection = 0
        while True:
            current_selection = self.display_menu(self.main_menu_menus, [0, 1, 2, 3, 4], current_selection, [[50, 120], [250, 280], [350, 380], [450, 480], [550, 580]])

            if current_selection == 0:
                self.white_score = 0
                self.black_score = 0
                return
            elif current_selection == 1:
                self.number_of_players = self.display_menu(self.number_of_players_menus, [0, 1, 2, self.number_of_players], self.number_of_players, [[245, 285], [345, 385], [445, 485], [545, 585]])
            elif current_selection == 2:
                self.ai_sleep_duration = self.display_menu(self.ai_speed_menus, [0, 1, 2, self.ai_sleep_duration], self.ai_sleep_duration, [[245, 285], [345, 385], [445, 485], [545, 585]])
            elif current_selection == 3:
                self.display_menu(self.info_menus, [0], 0, [[545, 585]])
            elif current_selection == 4:
                pygame.display.quit()
                sys.exit()

    def display_menu(self, option_menus, options, current_value, options_mouse_positions):
        current_selection = 0
        for i, val in enumerate(options):
            if val == current_value:
                current_selection = i
                break
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if current_selection == 0:
                            current_selection = len(options) - 2
                        else:
                            current_selection -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if current_selection == (len(options) - 2):
                            current_selection = 0
                        else:
                            current_selection += 1
                    elif event.key == pygame.K_q:
                        return options[-1]
                    elif self.game_is_over and event.key == pygame.K_r:
                        return False

                _, y = pygame.mouse.get_pos()

                if self.previous_mouse_position != pygame.mouse.get_pos():
                    for index, pos in enumerate(options_mouse_positions):
                        if pos[0] <= y <= pos[1]:
                            if current_selection != index:
                                self.menu_selection_sound.play()
                            current_selection = index
                            break

                if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    self.menu_selection_sound.play()
                    return options[current_selection]

            if self.game_is_over:
                if pygame.key.get_pressed()[pygame.K_h]:
                    self.display_board()
                else:
                    self.window.blit(self.game_over_menus[current_selection], (self.WINDOW_SIZE / 2 - self.GAME_OVER_WIDTH / 2, self.WINDOW_SIZE / 2 - self.GAME_OVER_HEIGHT / 2))

                    self.window.blit(self.current_score, self.current_score.get_rect(center=(self.WINDOW_SIZE / 2, self.WINDOW_SIZE / 2 - self.GAME_OVER_HEIGHT / 2 + self.PIECE_SIZE / 2 + 10)))

                    if self.chess_board.outcome().winner == chess.WHITE:
                        self.window.blit(self.game_outcomes[0], self.game_outcomes[0].get_rect(center=(self.WINDOW_SIZE / 2, 295)))
                    elif self.chess_board.outcome().winner == chess.BLACK:
                        self.window.blit(self.game_outcomes[1], self.game_outcomes[1].get_rect(center=(self.WINDOW_SIZE / 2, 295)))
                    else:  # Draw
                        self.window.blit(self.game_outcomes[self.chess_board.outcome().termination.value], self.game_outcomes[self.chess_board.outcome().termination.value].get_rect(center=(self.WINDOW_SIZE / 2, 295)))

                    pygame.display.update()
            else:
                self.previous_mouse_position = pygame.mouse.get_pos()
                self.window.blit(option_menus[current_selection], (0, 0))
                pygame.display.update()

    def display_game_over_menu(self):
        self.game_over_sound.play()

        if self.chess_board.outcome().winner == chess.WHITE:
            self.white_score += 1
        elif self.chess_board.outcome().winner == chess.BLACK:
            self.black_score += 1

        self.game_is_over = True

        self.current_score = self.GAME_OVER_SCORE_FONT.render(f'{self.white_score}-{self.black_score}', True, self.TEXT_COLOUR)

        return self.display_menu(self.game_over_menus, [False, True, True], False, [[340, 375], [390, 430]])

    def display_board(self):
        self.window.blit(self.blank_board, (0, 0))
        for i in range(64):
            if self.chess_board.piece_at(i) is not None:
                self.window.blit(self.piece_pngs[self.chess_board.piece_at(i).symbol()], self.get_coords_from_grid_pos(i, self.PIECE_PAD))

        if self.previous_moves_from and self.previous_moves_to:
            pygame.draw.rect(self.window, self.PREVIOUS_MOVE_FROM_COLOUR, self.get_rect_from_grid_pos(self.previous_moves_from[-1]))
            pygame.draw.rect(self.window, self.PREVIOUS_MOVE_TO_COLOUR, self.get_rect_from_grid_pos(self.previous_moves_to[-1]))
            self.window.blit(self.piece_pngs[self.previous_move_piece], self.get_coords_from_grid_pos(self.previous_moves_to[-1], self.PIECE_PAD))

        if self.chess_board.is_check():
            king_location = self.chess_board.king(self.chess_board.turn)
            pygame.draw.rect(self.window, self.KING_IN_CHECK_COLOUR, self.get_rect_from_grid_pos(king_location))
            self.window.blit(self.piece_pngs[self.chess_board.piece_at(king_location).symbol()], self.get_coords_from_grid_pos(king_location, self.PIECE_PAD))

        if self.mouse_button_down and self.selected_piece is not None:
            pygame.draw.rect(self.window, self.SELECTED_PIECE_COLOUR, self.get_rect_from_grid_pos(self.selected_piece_grid_pos))
            temp_surface = pygame.Surface((self.WINDOW_SIZE, self.WINDOW_SIZE), pygame.SRCALPHA)

            for move in list(self.chess_board.legal_moves):
                if move.from_square == self.selected_piece_grid_pos:
                    print(f"{self.chess_board.color_at(move.to_square)}   {self.chess_board.turn}")
                    if self.chess_board.color_at(move.to_square) is None:
                        pygame.draw.circle(temp_surface, self.LEGAL_MOVE_COLOUR, self.get_coords_from_grid_pos(move.to_square, self.SQUARE_SIZE / 2), self.LEGAL_MOVE_RADIUS)
                    elif self.chess_board.color_at(move.to_square) != self.chess_board.turn:
                        pygame.draw.circle(temp_surface, self.LEGAL_MOVE_CAPTURE_COLOUR, self.get_coords_from_grid_pos(move.to_square, self.SQUARE_SIZE / 2), self.LEGAL_MOVE_CAPTURE_RADIUS, self.LEGAL_MOVE_CAPTURE_WIDTH)

            self.window.blit(temp_surface, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            self.window.blit(self.piece_pngs[self.selected_piece.symbol()], (mouse_pos[0] - self.PIECE_SIZE / 2, mouse_pos[1] - self.PIECE_SIZE / 2))

        pygame.display.update()

    def get_next_move_from_user(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        pygame.display.quit()
                        sys.exit()
                    if event.key == pygame.K_BACKSPACE:
                        self.undo_move()
                    if event.key == pygame.K_q:
                        self.go_to_main_menu = True
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.selected_piece_grid_pos = self.get_grid_pos_from_coords(pygame.mouse.get_pos())
                    self.selected_piece = self.chess_board.piece_at(self.selected_piece_grid_pos)
                    self.mouse_button_down = True
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.new_grid_pos = self.get_grid_pos_from_coords(pygame.mouse.get_pos())
                    valid_move = self.execute_next_move()
                    self.selected_piece = None
                    self.selected_piece_grid_pos = None
                    self.mouse_button_down = False
                    if valid_move:
                        return

            self.display_board()
            pygame.display.update()

    def get_next_move_from_ai(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pygame.display.quit()
                    sys.exit()
                if event.key == pygame.K_q:
                    self.go_to_main_menu = True
                    return

        time.sleep(self.ai_sleep_duration)
        next_move = random.choice(list(self.chess_board.legal_moves))
        self.selected_piece = self.chess_board.piece_at(next_move.from_square)
        self.selected_piece_grid_pos = next_move.from_square
        self.new_grid_pos = next_move.to_square

        self.execute_next_move(current_turn_is_ai=True)

    def execute_next_move(self, current_turn_is_ai=False):
        try:
            self.chess_board.find_move(self.selected_piece_grid_pos, self.new_grid_pos)
        except ValueError:  # Illegal move
            return False

        if (self.selected_piece.symbol() == 'P' and math.floor(self.new_grid_pos / 8) == 7) or (self.selected_piece.symbol() == 'p' and math.floor(self.new_grid_pos / 8) == 0):
            next_move = chess.Move(self.selected_piece_grid_pos, self.new_grid_pos, self.get_pawn_promotion_choice(self.new_grid_pos, current_turn_is_ai))

            if self.ai_sleep_duration != 0 or self.number_of_players > 0:
                if self.chess_board.gives_check(next_move):
                    self.check_sound.play()
                elif self.chess_board.is_castling(next_move):
                    self.castling_sound.play()
                elif self.chess_board.piece_at(self.new_grid_pos) is not None:
                    self.capture_sound.play()
                else:
                    self.move_sound.play()

            self.chess_board.push(next_move)
        else:
            next_move = chess.Move(self.selected_piece_grid_pos, self.new_grid_pos)

            if self.ai_sleep_duration != 0 or self.number_of_players > 0:
                if self.chess_board.gives_check(next_move):
                    self.check_sound.play()
                elif self.chess_board.is_castling(next_move):
                    self.castling_sound.play()
                elif self.chess_board.piece_at(self.new_grid_pos) is not None:
                    self.capture_sound.play()
                else:
                    self.move_sound.play()

            self.chess_board.push(next_move)

        self.previous_moves_from.append(self.selected_piece_grid_pos)
        self.previous_moves_to.append(self.new_grid_pos)
        self.previous_move_piece = self.chess_board.piece_at(self.previous_moves_to[-1]).symbol()

        return True

    def undo_move(self):
        try:
            self.chess_board.pop()
            self.previous_moves_from.pop()
            self.previous_moves_to.pop()
            self.previous_move_piece = self.chess_board.piece_at(self.previous_moves_to[-1]).symbol()
        except IndexError:  # No moves to undo
            pass

    def get_pawn_promotion_choice(self, new_grid_pos, current_turn_is_ai):
        if current_turn_is_ai:
            return random.choice([chess.QUEEN, chess.KNIGHT, chess.ROOK, chess.BISHOP])

        x = self.SQUARE_SIZE * (new_grid_pos % 8) + self.PIECE_PAD
        if self.chess_board.turn == chess.WHITE:
            pygame.draw.rect(self.window, self.PAWN_PROMOTION_BG, (x - self.PIECE_PAD, 0, self.SQUARE_SIZE, self.SQUARE_SIZE * 4))
            self.window.blit(self.piece_pngs['Q'], (x, self.PIECE_PAD + self.SQUARE_SIZE * 0))
            self.window.blit(self.piece_pngs['N'], (x, self.PIECE_PAD + self.SQUARE_SIZE * 1))
            self.window.blit(self.piece_pngs['R'], (x, self.PIECE_PAD + self.SQUARE_SIZE * 2))
            self.window.blit(self.piece_pngs['B'], (x, self.PIECE_PAD + self.SQUARE_SIZE * 3))
        else:
            pygame.draw.rect(self.window, self.PAWN_PROMOTION_BG,
                             (x - self.PIECE_PAD, self.WINDOW_SIZE - self.SQUARE_SIZE * 4, self.SQUARE_SIZE, self.SQUARE_SIZE * 4))
            self.window.blit(self.piece_pngs['q'], (x, self.WINDOW_SIZE + self.PIECE_PAD - self.SQUARE_SIZE * 1))
            self.window.blit(self.piece_pngs['n'], (x, self.WINDOW_SIZE + self.PIECE_PAD - self.SQUARE_SIZE * 2))
            self.window.blit(self.piece_pngs['r'], (x, self.WINDOW_SIZE + self.PIECE_PAD - self.SQUARE_SIZE * 3))
            self.window.blit(self.piece_pngs['b'], (x, self.WINDOW_SIZE + self.PIECE_PAD - self.SQUARE_SIZE * 4))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        pygame.display.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    x = int(pygame.mouse.get_pos()[0] / self.SQUARE_SIZE)
                    y = int(pygame.mouse.get_pos()[1] / self.SQUARE_SIZE)
                    if x == (new_grid_pos % 8):
                        if self.chess_board.turn == chess.WHITE:
                            if y == 0:
                                return chess.QUEEN
                            elif y == 1:
                                return chess.KNIGHT
                            elif y == 2:
                                return chess.ROOK
                            elif y == 3:
                                return chess.BISHOP
                        else:
                            if y == 7:
                                return chess.QUEEN
                            elif y == 6:
                                return chess.KNIGHT
                            elif y == 5:
                                return chess.ROOK
                            elif y == 4:
                                return chess.BISHOP

    def get_grid_pos_from_coords(self, coords):
        return 8 * (7 - int(coords[1] / self.SQUARE_SIZE)) + int(coords[0] / self.SQUARE_SIZE)

    def get_coords_from_grid_pos(self, grid_pos, pad):
        return (grid_pos % 8) * self.SQUARE_SIZE + pad, (7 - int(grid_pos / 8)) * self.SQUARE_SIZE + pad

    def get_rect_from_grid_pos(self, grid_pos):
        return (grid_pos % 8) * self.SQUARE_SIZE, (7 - int(grid_pos / 8)) * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE

    def create_blank_board(self):
        blank_board = pygame.Surface((self.WINDOW_SIZE, self.WINDOW_SIZE))
        blank_board.fill(self.WINDOW_BG_DARK)
        draw_light_rect = False
        for y in range(0, self.WINDOW_SIZE, self.SQUARE_SIZE):
            for x in range(0, self.WINDOW_SIZE, self.SQUARE_SIZE):
                if draw_light_rect:
                    pygame.draw.rect(blank_board, self.WINDOW_BG_LIGHT, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))
                draw_light_rect = not draw_light_rect
            draw_light_rect = not draw_light_rect
        return blank_board

    def create_menus(self, txt, txt_x, txt_y_title, txt_y_body, txt_y_body_diff, title_font, body_font, selection_start, selection_end):
        fonts = [title_font]
        for i in range(1, len(txt)):
            fonts.append(body_font)

        menus = []
        for i in range(selection_start, selection_end + 1):
            menu = pygame.Surface((self.WINDOW_SIZE, self.WINDOW_SIZE))
            menu.fill(self.MENU_WINDOW_BG)
            for j in range(len(txt)):
                if j == i:
                    if j == 0:
                        menu.blit(fonts[0].render(txt[0], True, self.SELECTED_TEXT_COLOUR), (txt_x, txt_y_title))
                    else:
                        menu.blit(fonts[j].render(txt[j], True, self.SELECTED_TEXT_COLOUR),
                                  (txt_x, txt_y_body + txt_y_body_diff * j))
                else:
                    if j == 0:
                        menu.blit(fonts[0].render(txt[0], True, self.TEXT_COLOUR), (txt_x, txt_y_title))
                    else:
                        menu.blit(fonts[j].render(txt[j], True, self.TEXT_COLOUR),
                                  (txt_x, txt_y_body + txt_y_body_diff * j))
            menus.append(menu)

        return menus

    def create_info_menu(self):
        info_menu = pygame.Surface((self.WINDOW_SIZE, self.WINDOW_SIZE))
        info_menu.fill(self.MENU_WINDOW_BG)
        info_menu.blit(self.INFO_MENU_TITLE_FONT.render('INFORMATION', True, self.TEXT_COLOUR), (50, 50))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render(' USE THE MOUSE TO DRAG AND DROP PIECES', True, self.TEXT_COLOUR), (50, 150))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render(' ALL LEGAL MOVES ARE SHOWN FOR A SELECTED PIECE', True, self.TEXT_COLOUR), (50, 190))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render(' ALL CHESS RULES ENFORCED VIA python-chess LIBRARY', True, self.TEXT_COLOUR), (50, 230))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render(' BACKSPACE = UNDO MOVE', True, self.TEXT_COLOUR), (50, 270))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render(' H = HIDE GAME OVER MESSAGE', True, self.TEXT_COLOUR), (50, 310))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render(' R = RESTART WHEN GAMER OVER', True, self.TEXT_COLOUR), (50, 350))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render(' Q = QUIT TO MAIN MENU WHEN IN GAME', True, self.TEXT_COLOUR), (50, 390))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render(' Q = GO BACK IN SUBMENUS', True, self.TEXT_COLOUR), (50, 430))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render(' Q = QUIT PROGRAM WHEN IN MAIN MENU', True, self.TEXT_COLOUR), (50, 470))
        info_menu.blit(self.INFO_MENU_RETURN_FONT.render(' BACK TO MAIN MENU', True, self.SELECTED_TEXT_COLOUR), (50, 550))

        return [info_menu]

    def create_game_over_menu(self):
        rematch_text_selected = self.GAME_OVER_TITLE_FONT.render('REMATCH', True, self.SELECTED_TEXT_COLOUR)
        quit_text_selected = self.GAME_OVER_TITLE_FONT.render('QUIT', True, self.SELECTED_TEXT_COLOUR)
        rematch_text = self.GAME_OVER_TITLE_FONT.render('REMATCH', True, self.TEXT_COLOUR)
        quit_text = self.GAME_OVER_TITLE_FONT.render('QUIT', True, self.TEXT_COLOUR)

        rematch = pygame.Surface((self.GAME_OVER_WIDTH, self.GAME_OVER_HEIGHT))
        rematch.fill(self.MENU_WINDOW_BG)
        rematch.blit(rematch_text_selected, rematch_text_selected.get_rect(center=(self.GAME_OVER_WIDTH / 2, self.GAME_OVER_HEIGHT - 85)))
        rematch.blit(quit_text, quit_text.get_rect(center=(self.GAME_OVER_WIDTH / 2, self.GAME_OVER_HEIGHT - 35)))
        rematch.blit(self.piece_pngs['K'], (self.GAME_OVER_WIDTH / 2 - self.PIECE_SIZE - 50, 0))
        rematch.blit(self.piece_pngs['k'], (self.GAME_OVER_WIDTH / 2 + 50, 0))

        quit_game = pygame.Surface((self.GAME_OVER_WIDTH, self.GAME_OVER_HEIGHT))
        quit_game.fill(self.MENU_WINDOW_BG)
        quit_game.blit(rematch_text, rematch_text.get_rect(center=(self.GAME_OVER_WIDTH / 2, self.GAME_OVER_HEIGHT - 85)))
        quit_game.blit(quit_text_selected, quit_text_selected.get_rect(center=(self.GAME_OVER_WIDTH / 2, self.GAME_OVER_HEIGHT - 35)))
        quit_game.blit(self.piece_pngs['K'], (self.GAME_OVER_WIDTH / 2 - self.PIECE_SIZE - 50, 0))
        quit_game.blit(self.piece_pngs['k'], (self.GAME_OVER_WIDTH / 2 + 50, 0))

        return [rematch, quit_game]
