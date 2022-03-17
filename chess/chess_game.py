import os
import sys
import time
import random
import pygame
import chess


class App:
    def __init__(self):
        self.window_size = 640
        self.pieces_size = 88
        self.square_size = int(self.window_size / 8)
        self.piece_pad = int((self.square_size - self.pieces_size) / 2)

        pygame.init()
        pygame.display.set_caption('Chess')
        pygame.display.set_icon(pygame.image.load(self.get_path('app.ico')))
        self.window = pygame.display.set_mode((self.window_size, self.window_size))

        self.game_over_width = 350
        self.game_over_height = 250

        self.window_bg_dark = (81, 42, 42)
        self.window_bg_light = (124, 76, 62)
        self.menu_window_bg = (8, 8, 8)
        self.pawn_promotion_bg = (162, 84, 84)

        self.piece_selected_colour = (192, 192, 75)
        self.previous_move_from_colour = (128, 128, 50)
        self.previous_move_to_colour = (192, 192, 75)

        self.king_in_check_colour = (247, 119, 105)

        self.legal_move_colour = (255, 255, 255, 100)
        self.legal_move_capture_colour = (255, 0, 0, 100)
        self.legal_move_radius = 12
        self.legal_move_capture_radius = self.square_size / 2
        self.legal_move_capture_width = 8

        self.text_colour = (255, 255, 255)
        self.selected_text_colour = (0, 156, 128)

        self.main_font = 'Video Game Font'
        self.main_menu_title_font = pygame.font.SysFont(self.main_font, 120)
        self.sub_menu_title_font = pygame.font.SysFont(self.main_font, 90)
        self.menu_options_font = pygame.font.SysFont(self.main_font, 48)

        self.info_menu_title_font = pygame.font.SysFont(self.main_font, 90)
        self.info_menu_body_font = pygame.font.SysFont(self.main_font, 28)
        self.info_menu_return_font = pygame.font.SysFont(self.main_font, 48)

        self.game_over_font = pygame.font.SysFont(self.main_font, 48)
        self.game_over_outcome_font = pygame.font.SysFont(self.main_font, 20)
        self.game_over_score_font = pygame.font.SysFont(self.main_font, 72)

        self.number_of_players = 1
        self.ai_sleep_duration = 1
        self.human_player = chess.WHITE

        self.new_grid_pos = None
        self.previous_mouse_position = (0, 0)

        self.start_sound = pygame.mixer.Sound(self.get_path('start.wav'))
        self.move_sound = pygame.mixer.Sound(self.get_path('move.wav'))
        self.castling_sound = pygame.mixer.Sound(self.get_path('castling.wav'))
        self.capture_sound = pygame.mixer.Sound(self.get_path('capture.wav'))
        self.check_sound = pygame.mixer.Sound(self.get_path('check.wav'))
        self.game_over_sound = pygame.mixer.Sound(self.get_path('game over.wav'))

        self.piecePNGs = {
            'K': pygame.transform.smoothscale(pygame.image.load(self.get_path('white king.png')), (self.pieces_size, self.pieces_size)),
            'Q': pygame.transform.smoothscale(pygame.image.load(self.get_path('white queen.png')), (self.pieces_size, self.pieces_size)),
            'B': pygame.transform.smoothscale(pygame.image.load(self.get_path('white bishop.png')), (self.pieces_size, self.pieces_size)),
            'R': pygame.transform.smoothscale(pygame.image.load(self.get_path('white rook.png')), (self.pieces_size, self.pieces_size)),
            'N': pygame.transform.smoothscale(pygame.image.load(self.get_path('white knight.png')), (self.pieces_size, self.pieces_size)),
            'P': pygame.transform.smoothscale(pygame.image.load(self.get_path('white pawn.png')), (self.pieces_size, self.pieces_size)),
            'k': pygame.transform.smoothscale(pygame.image.load(self.get_path('black king.png')), (self.pieces_size, self.pieces_size)),
            'q': pygame.transform.smoothscale(pygame.image.load(self.get_path('black queen.png')), (self.pieces_size, self.pieces_size)),
            'b': pygame.transform.smoothscale(pygame.image.load(self.get_path('black bishop.png')), (self.pieces_size, self.pieces_size)),
            'r': pygame.transform.smoothscale(pygame.image.load(self.get_path('black rook.png')), (self.pieces_size, self.pieces_size)),
            'n': pygame.transform.smoothscale(pygame.image.load(self.get_path('black knight.png')), (self.pieces_size, self.pieces_size)),
            'p': pygame.transform.smoothscale(pygame.image.load(self.get_path('black pawn.png')), (self.pieces_size, self.pieces_size)),
        }

        self.gameOutcomes = [
            self.game_over_outcome_font.render('(WHITE WINS)', True, self.text_colour),
            self.game_over_outcome_font.render('(BLACK WINS)', True, self.text_colour),
            self.game_over_outcome_font.render('(DRAW DUE TO STALEMATE)', True, self.text_colour),
            self.game_over_outcome_font.render('(DRAW DUE TO INSUFFICIENT MATERIAL)', True, self.text_colour),
            self.game_over_outcome_font.render('(DRAW DUE TO SEVENTY FIVE MOVES RULE)', True, self.text_colour),
            self.game_over_outcome_font.render('(DRAW DUE TO FIVEFOLD REPETITION RULE)', True, self.text_colour),
            self.game_over_outcome_font.render('(DRAW DUE TO FIFTY MOVES RULE)', True, self.text_colour),
            self.game_over_outcome_font.render('(DRAW DUE TO THREEFOLD REPETITION RULE)', True, self.text_colour),
        ]

        self.blank_board = self.create_blank_board()
        self.main_menus = self.create_menus(['PLAY CHESS', ' NO. OF PLAYERS', ' AI SPEED', ' INFO', ' QUIT'],
                                            50, 50, 150, 100, self.main_menu_title_font, self.menu_options_font, 0, 4)
        self.number_of_players_menus = self.create_menus(['NO. OF PLAYERS', ' 0', ' 1', ' 2', ' BACK TO MAIN MENU'],
                                                         50, 50, 150, 100, self.sub_menu_title_font, self.menu_options_font, 1, 4)
        self.ai_speed_menus = self.create_menus(['AI SPEED', ' 0', ' 1', ' 2', ' BACK TO MAIN MENU'],
                                                50, 50, 150, 100, self.sub_menu_title_font, self.menu_options_font, 1, 4)
        self.info_menu = self.create_info_menu()
        self.game_over_menu = self.create_game_over_menu()

        # Game Loop
        self.go_to_main_menu = True
        while True:
            if self.go_to_main_menu:
                self.display_main_menu()
                self.white_score = 0
                self.black_score = 0

            self.mouse_button_down = False
            self.selected_piece_grid_pos = None
            self.selected_piece = None

            self.previous_moves_from = []
            self.previous_moves_to = []
            self.previous_move_piece = None

            self.chess_board = chess.Board()

            self.go_immediately_to_main_menu = False
            self.start_sound.play()
            while self.chess_board.outcome() is None and not self.go_immediately_to_main_menu:
                self.display_board()
                pygame.display.update()

                if self.number_of_players == 2:
                    self.next_turn_is_AI = False
                    self.get_next_move_from_user()
                elif self.number_of_players == 1:
                    if self.chess_board.turn == self.human_player:
                        self.next_turn_is_AI = False
                        self.get_next_move_from_user()
                    else:
                        self.next_turn_is_AI = True
                        self.get_next_move_from_ai()
                elif self.number_of_players == 0:
                    self.next_turn_is_AI = True
                    self.get_next_move_from_ai()

                self.display_board()
                pygame.display.update()

            if not self.go_immediately_to_main_menu:
                self.game_over_sound.play()
                self.go_to_main_menu = self.display_game_over_menu()

    # noinspection PyMethodMayBeStatic
    def get_path(self, file_name):
        try:
            # noinspection PyProtectedMember
            return os.path.join(sys._MEIPASS, file_name)
        except AttributeError:
            return 'chess\\resources\\' + file_name

    def get_grid_pos_from_coords(self, coords):
        return 8 * (7 - int(coords[1] / self.square_size)) + int(coords[0] / self.square_size)

    def get_coords_from_grid_pos(self, grid_pos, pad):
        return (grid_pos % 8) * self.square_size + pad, (7 - int(grid_pos / 8)) * self.square_size + pad

    def get_rect_from_grid_pos(self, grid_pos):
        return (grid_pos % 8) * self.square_size, (7 - int(grid_pos / 8)) * self.square_size, self.square_size, self.square_size

    def create_blank_board(self):
        blank_board = pygame.Surface((self.window_size, self.window_size))
        blank_board.fill(self.window_bg_dark)
        draw_light_rect = False
        for y in range(0, self.window_size, self.square_size):
            for x in range(0, self.window_size, self.square_size):
                if draw_light_rect:
                    pygame.draw.rect(blank_board, self.window_bg_light, (x, y, self.square_size, self.square_size))
                draw_light_rect = not draw_light_rect
            draw_light_rect = not draw_light_rect
        return blank_board

    def create_menus(self, txt, txt_x, txt_y_title, txt_y_body, txt_y_body_diff, title_font, body_font, selection_start, selection_end):
        fonts = [title_font]
        for i in range(1, len(txt)):
            fonts.append(body_font)

        menus = []
        for i in range(selection_start, selection_end + 1):
            menu = pygame.Surface((self.window_size, self.window_size))
            menu.fill(self.menu_window_bg)
            for j in range(len(txt)):
                if j == i:
                    if j == 0:
                        menu.blit(fonts[0].render(txt[0], True, self.selected_text_colour), (txt_x, txt_y_title))
                    else:
                        menu.blit(fonts[j].render(txt[j], True, self.selected_text_colour),
                                  (txt_x, txt_y_body + txt_y_body_diff * j))
                else:
                    if j == 0:
                        menu.blit(fonts[0].render(txt[0], True, self.text_colour), (txt_x, txt_y_title))
                    else:
                        menu.blit(fonts[j].render(txt[j], True, self.text_colour),
                                  (txt_x, txt_y_body + txt_y_body_diff * j))
            menus.append(menu)

        return menus

    def create_info_menu(self):
        info_menu = pygame.Surface((self.window_size, self.window_size))

        info_menu.fill(self.menu_window_bg)
        info_menu.blit(self.info_menu_title_font.render('INFORMATION', True, self.text_colour), (50, 50))
        info_menu.blit(self.info_menu_body_font.render(' USE THE MOUSE TO DRAG AND DROP PIECES', True, self.text_colour), (50, 150))
        info_menu.blit(self.info_menu_body_font.render(' ALL LEGAL MOVES ARE SHOWN FOR A SELECTED PIECE', True, self.text_colour), (50, 190))
        info_menu.blit(self.info_menu_body_font.render(' ALL CHESS RULES ENFORCED VIA python-chess LIBRARY', True, self.text_colour), (50, 230))
        info_menu.blit(self.info_menu_body_font.render(' BACKSPACE = UNDO MOVE', True, self.text_colour), (50, 270))
        info_menu.blit(self.info_menu_body_font.render(' H = HIDE GAME OVER MESSAGE', True, self.text_colour), (50, 310))
        info_menu.blit(self.info_menu_body_font.render(' R = RESTART WHEN GAMER OVER', True, self.text_colour), (50, 350))
        info_menu.blit(self.info_menu_body_font.render(' Q = QUIT TO MAIN MENU WHEN IN GAME', True, self.text_colour), (50, 390))
        info_menu.blit(self.info_menu_body_font.render(' Q = GO BACK IN SUBMENUS', True, self.text_colour), (50, 430))
        info_menu.blit(self.info_menu_body_font.render(' Q = QUIT PROGRAM WHEN IN MAIN MENU', True, self.text_colour), (50, 470))
        info_menu.blit(self.info_menu_return_font.render(' BACK TO MAIN MENU', True, self.selected_text_colour), (50, 550))

        return info_menu

    def create_game_over_menu(self):
        rematch_text_selected = self.game_over_font.render('REMATCH', True, self.selected_text_colour)
        quit_text_selected = self.game_over_font.render('QUIT', True, self.selected_text_colour)
        rematch_text = self.game_over_font.render('REMATCH', True, self.text_colour)
        quit_text = self.game_over_font.render('QUIT', True, self.text_colour)

        rematch = pygame.Surface((self.game_over_width, self.game_over_height))
        rematch.fill(self.menu_window_bg)
        rematch.blit(rematch_text_selected, rematch_text_selected.get_rect(center=(self.game_over_width / 2, self.game_over_height - 85)))
        rematch.blit(quit_text, quit_text.get_rect(center=(self.game_over_width / 2, self.game_over_height - 35)))
        rematch.blit(self.piecePNGs['K'], (self.game_over_width / 2 - self.pieces_size - 50, 0))
        rematch.blit(self.piecePNGs['k'], (self.game_over_width / 2 + 50, 0))

        quit_game = pygame.Surface((self.game_over_width, self.game_over_height))
        quit_game.fill(self.menu_window_bg)
        quit_game.blit(rematch_text, rematch_text.get_rect(center=(self.game_over_width / 2, self.game_over_height - 85)))
        quit_game.blit(quit_text_selected, quit_text_selected.get_rect(center=(self.game_over_width / 2, self.game_over_height - 35)))
        quit_game.blit(self.piecePNGs['K'], (self.game_over_width / 2 - self.pieces_size - 50, 0))
        quit_game.blit(self.piecePNGs['k'], (self.game_over_width / 2 + 50, 0))

        return [rematch, quit_game]

    def display_main_menu(self):
        current_selection = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if current_selection == 0:
                            current_selection = 4
                        else:
                            current_selection -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if current_selection == 4:
                            current_selection = 0
                        else:
                            current_selection += 1
                    elif event.key == pygame.K_q:
                        pygame.display.quit()
                        sys.exit()

                _, y = pygame.mouse.get_pos()

                if self.previous_mouse_position != pygame.mouse.get_pos():
                    if 50 <= y <= 120:
                        current_selection = 0
                    elif 250 <= y <= 280:
                        current_selection = 1
                    elif 350 <= y <= 380:
                        current_selection = 2
                    elif 450 <= y <= 480:
                        current_selection = 3
                    elif 550 <= y <= 580:
                        current_selection = 4

                if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    if current_selection == 0:
                        return
                    elif current_selection == 1:
                        self.display_number_of_players_options_menu()
                    elif current_selection == 2:
                        self.display_ai_speed_options_menu()
                    elif current_selection == 3:
                        self.display_info_menu()
                    elif current_selection == 4:
                        pygame.display.quit()
                        sys.exit()

            self.previous_mouse_position = pygame.mouse.get_pos()

            self.window.blit(self.main_menus[current_selection], (0, 0))

            pygame.display.update()

    def display_number_of_players_options_menu(self):
        current_selection = self.number_of_players
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if current_selection == 0:
                            current_selection = 3
                        else:
                            current_selection -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if current_selection == 3:
                            current_selection = 0
                        else:
                            current_selection += 1
                    elif event.key == pygame.K_RETURN:
                        if current_selection != 3:
                            self.number_of_players = current_selection
                        return
                    elif event.key == pygame.K_q:
                        return

                _, y = pygame.mouse.get_pos()

                if self.previous_mouse_position != pygame.mouse.get_pos():
                    if 245 <= y <= 285:
                        current_selection = 0
                    elif 345 <= y <= 385:
                        current_selection = 1
                    elif 445 <= y <= 485:
                        current_selection = 2
                    elif 540 <= y <= 580:
                        current_selection = 3

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if current_selection != 3:
                        self.number_of_players = current_selection
                    return

            self.previous_mouse_position = pygame.mouse.get_pos()

            self.window.blit(self.number_of_players_menus[current_selection], (0, 0))

            pygame.display.update()

    def display_ai_speed_options_menu(self):
        current_selection = self.ai_sleep_duration
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if current_selection == 0:
                            current_selection = 3
                        else:
                            current_selection -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if current_selection == 3:
                            current_selection = 0
                        else:
                            current_selection += 1
                    elif event.key == pygame.K_RETURN:
                        self.ai_sleep_duration = current_selection
                        return
                    elif event.key == pygame.K_q:
                        return

                _, y = pygame.mouse.get_pos()

                if self.previous_mouse_position != pygame.mouse.get_pos():
                    if 245 <= y <= 285:
                        current_selection = 0
                    elif 345 <= y <= 385:
                        current_selection = 1
                    elif 445 <= y <= 485:
                        current_selection = 2
                    elif 540 <= y <= 580:
                        current_selection = 3

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.ai_sleep_duration = current_selection
                    return

            self.previous_mouse_position = pygame.mouse.get_pos()

            self.window.blit(self.ai_speed_menus[current_selection], (0, 0))

            pygame.display.update()

    def display_info_menu(self):
        self.window.blit(self.info_menu, (0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_RETURN):
                    return
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    _, y = pygame.mouse.get_pos()
                    if 540 <= y <= 580:
                        return

            pygame.display.update()

    def display_game_over_menu(self):
        if self.chess_board.outcome().winner == chess.WHITE:
            self.white_score += 1
        elif self.chess_board.outcome().winner == chess.BLACK:
            self.black_score += 1

        score = self.game_over_score_font.render(f'{self.white_score}-{self.black_score}', True, self.text_colour)
        current_selection = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if current_selection == 0:
                            current_selection = 1
                        else:
                            current_selection -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if current_selection == 1:
                            current_selection = 0
                        else:
                            current_selection += 1
                    elif event.key == pygame.K_RETURN:
                        if current_selection == 0:
                            return False
                        elif current_selection == 1:
                            return True
                    elif event.key == pygame.K_r:
                        return False
                    elif event.key == pygame.K_q:
                        return True

                _, y = pygame.mouse.get_pos()

                if self.previous_mouse_position != pygame.mouse.get_pos():
                    if 340 <= y <= 375:
                        current_selection = 0
                    elif 390 <= y <= 430:
                        current_selection = 1

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if current_selection == 0:
                        return False
                    elif current_selection == 1:
                        return True

            if not pygame.key.get_pressed()[pygame.K_h]:
                self.window.blit(self.game_over_menu[current_selection],
                                 (self.window_size / 2 - self.game_over_width / 2, self.window_size / 2 - self.game_over_height / 2))

                self.window.blit(score,
                                 score.get_rect(
                                     center=(self.window_size / 2, self.window_size / 2 - self.game_over_height / 2 + self.pieces_size / 2 + 10)))

                if self.chess_board.outcome().winner == chess.WHITE:

                    self.window.blit(self.gameOutcomes[0], self.gameOutcomes[0].get_rect(center=(self.window_size / 2, 295)))
                elif self.chess_board.outcome().winner == chess.BLACK:
                    self.window.blit(self.gameOutcomes[1], self.gameOutcomes[1].get_rect(center=(self.window_size / 2, 295)))
                else:  # Draw
                    self.window.blit(self.gameOutcomes[self.chess_board.outcome().termination.value],
                                     self.gameOutcomes[self.chess_board.outcome().termination.value].get_rect(center=(self.window_size / 2, 295)))
            else:
                self.display_board()

            self.previous_mouse_position = pygame.mouse.get_pos()

            pygame.display.update()

    def get_selected_piece_and_pos(self):
        piece_grid_pos = self.get_grid_pos_from_coords(pygame.mouse.get_pos())
        piece = self.chess_board.piece_at(piece_grid_pos)
        if piece is None:
            piece_symbol = None
        else:
            if piece.color == self.chess_board.turn:
                piece_symbol = piece.symbol()
            else:
                piece_symbol = None

        return piece_symbol, piece_grid_pos,

    def execute_next_move(self):
        try:
            self.chess_board.find_move(self.selected_piece_grid_pos, self.new_grid_pos)
        except ValueError:  # Illegal move
            return False

        if (self.selected_piece == 'P' and int(self.new_grid_pos / 8) == 7) or (self.selected_piece == 'p' and int(self.new_grid_pos / 8) == 0):
            next_move = chess.Move(self.selected_piece_grid_pos, self.new_grid_pos, self.get_pawn_promotion_choice(self.new_grid_pos))

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

    def get_pawn_promotion_choice(self, new_grid_pos):
        if self.next_turn_is_AI:
            return random.choice([chess.QUEEN, chess.KNIGHT, chess.ROOK, chess.BISHOP])

        x = self.square_size * (new_grid_pos % 8) + self.piece_pad
        if self.chess_board.turn == chess.WHITE:
            pygame.draw.rect(self.window, self.pawn_promotion_bg, (x - self.piece_pad, 0, self.square_size, self.square_size * 4))
            self.window.blit(self.piecePNGs['Q'], (x, self.piece_pad + self.square_size * 0))
            self.window.blit(self.piecePNGs['N'], (x, self.piece_pad + self.square_size * 1))
            self.window.blit(self.piecePNGs['R'], (x, self.piece_pad + self.square_size * 2))
            self.window.blit(self.piecePNGs['B'], (x, self.piece_pad + self.square_size * 3))
        else:
            pygame.draw.rect(self.window, self.pawn_promotion_bg,
                             (x - self.piece_pad, self.window_size - self.square_size * 4, self.square_size, self.square_size * 4))
            self.window.blit(self.piecePNGs['q'], (x, self.window_size + self.piece_pad - self.square_size * 1))
            self.window.blit(self.piecePNGs['n'], (x, self.window_size + self.piece_pad - self.square_size * 2))
            self.window.blit(self.piecePNGs['r'], (x, self.window_size + self.piece_pad - self.square_size * 3))
            self.window.blit(self.piecePNGs['b'], (x, self.window_size + self.piece_pad - self.square_size * 4))

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
                    x = int(pygame.mouse.get_pos()[0] / self.square_size)
                    y = int(pygame.mouse.get_pos()[1] / self.square_size)
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

    def undo_move(self):
        try:
            self.chess_board.pop()
            self.previous_moves_from.pop()
            self.previous_moves_to.pop()
            self.previous_move_piece = self.chess_board.piece_at(self.previous_moves_to[-1]).symbol()
        except IndexError:  # No moves to undo
            pass

    def display_board(self):
        self.window.blit(self.blank_board, (0, 0))
        for i in range(64):
            if self.chess_board.piece_at(i) is not None:
                self.window.blit(self.piecePNGs[self.chess_board.piece_at(i).symbol()], self.get_coords_from_grid_pos(i, self.piece_pad))

        if self.previous_moves_from and self.previous_moves_to:
            pygame.draw.rect(self.window, self.previous_move_from_colour, self.get_rect_from_grid_pos(self.previous_moves_from[-1]))
            pygame.draw.rect(self.window, self.previous_move_to_colour, self.get_rect_from_grid_pos(self.previous_moves_to[-1]))
            self.window.blit(self.piecePNGs[self.previous_move_piece], self.get_coords_from_grid_pos(self.previous_moves_to[-1], self.piece_pad))

        if self.chess_board.is_check():
            kingLocation = self.chess_board.king(self.chess_board.turn)
            pygame.draw.rect(self.window, self.king_in_check_colour, self.get_rect_from_grid_pos(kingLocation))
            self.window.blit(self.piecePNGs[self.chess_board.piece_at(kingLocation).symbol()],
                             self.get_coords_from_grid_pos(kingLocation, self.piece_pad))

        if self.mouse_button_down and self.selected_piece is not None:
            pygame.draw.rect(self.window, self.piece_selected_colour, self.get_rect_from_grid_pos(self.selected_piece_grid_pos))
            tempSurface = pygame.Surface((self.window_size, self.window_size), pygame.SRCALPHA)

            for move in list(self.chess_board.legal_moves):
                if move.from_square == self.selected_piece_grid_pos:
                    if (self.chess_board.color_at(move.to_square) == chess.BLACK and self.chess_board.turn == chess.WHITE) or (
                            self.chess_board.color_at(move.to_square) == chess.WHITE and self.chess_board.turn == chess.BLACK):
                        pygame.draw.circle(tempSurface, self.legal_move_capture_colour,
                                           self.get_coords_from_grid_pos(move.to_square, self.square_size / 2),
                                           self.legal_move_capture_radius, self.legal_move_capture_width)
                    else:
                        pygame.draw.circle(tempSurface, self.legal_move_colour,
                                           self.get_coords_from_grid_pos(move.to_square, self.square_size / 2), self.legal_move_radius)

            self.window.blit(tempSurface, (0, 0))
            mousePos = pygame.mouse.get_pos()
            self.window.blit(self.piecePNGs[self.selected_piece], (mousePos[0] - self.pieces_size / 2, mousePos[1] - self.pieces_size / 2))

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
                        self.go_immediately_to_main_menu = True
                        self.go_to_main_menu = True
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.selected_piece, self.selected_piece_grid_pos = self.get_selected_piece_and_pos()
                    self.mouse_button_down = True
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.new_grid_pos = self.get_grid_pos_from_coords(pygame.mouse.get_pos())
                    validMove = self.execute_next_move()
                    self.selected_piece = None
                    self.selected_piece_grid_pos = None
                    self.mouse_button_down = False
                    if validMove:
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
                    self.go_immediately_to_main_menu = True
                    self.go_to_main_menu = True
                    return

        time.sleep(self.ai_sleep_duration)
        next_move = random.choice(list(self.chess_board.legal_moves))
        self.selected_piece = self.chess_board.piece_at(next_move.from_square)
        self.selected_piece_grid_pos = next_move.from_square
        self.new_grid_pos = next_move.to_square

        self.execute_next_move()
