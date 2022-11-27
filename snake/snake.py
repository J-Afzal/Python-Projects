import os
import sys
import time
import random
import pygame


class Snake:
    def __init__(self):
        pygame.init()

        # Constants
        self.GAME_WINDOW_SIZE = 640
        self.INFO_HEIGHT = 128
        self.WINDOW_WIDTH = self.GAME_WINDOW_SIZE
        self.WINDOW_HEIGHT = self.GAME_WINDOW_SIZE + self.INFO_HEIGHT
        self.WINDOW_MID_X = self.WINDOW_WIDTH / 2
        self.WINDOW_MID_Y = self.GAME_WINDOW_SIZE / 2 + self.INFO_HEIGHT

        self.GAME_OVER_WIDTH = 350
        self.GAME_OVER_HEIGHT = 250

        self.WINDOW_BG_DARK = (16, 16, 16)
        self.WINDOW_BG_LIGHT = (24, 24, 24)
        self.MENU_WINDOW_BG = (8, 8, 8)

        self.TEXT_COLOUR = (255, 255, 255)
        self.SELECTED_TEXT_COLOUR = (0, 128, 156)

        self.COLOUR_MIN = 32
        self.COLOUR_MAX = 196

        self.FONT = "Video Game Font"
        self.MAIN_MENU_TITLE_FONT = pygame.font.SysFont(self.FONT, 110)
        self.SUB_MENU_TITLE_FONT = pygame.font.SysFont(self.FONT, 72)
        self.MENU_OPTIONS_FONT = pygame.font.SysFont(self.FONT, 48)

        self.INFO_MENU_TITLE_FONT = pygame.font.SysFont(self.FONT, 72)
        self.INFO_MENU_BODY_FONT = pygame.font.SysFont(self.FONT, 32)
        self.INFO_MENU_RETURN_FONT = pygame.font.SysFont(self.FONT, 48)

        self.GAME_OVER_TITLE_FONT = pygame.font.SysFont(self.FONT, 72)
        self.GAME_OVER_OPTIONS_FONT = pygame.font.SysFont(self.FONT, 48)

        self.SNAKE_SCORE_FONT = pygame.font.SysFont(self.FONT, 48)
        self.SNAKE_FONT = pygame.font.SysFont(self.FONT, 32)

        # Variables
        pygame.display.set_caption("Snake")
        pygame.display.set_icon(pygame.image.load(self.get_path("app.ico")))
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.square_size = 32
        self.snake_speed = 10
        self.number_of_apples = 3

        self.snake_direction = None
        self.snake_points_x = None
        self.snake_points_y = None
        self.apple_positions = []

        self.start_time = None
        self.elapsed_time = None
        self.game_is_over = None
        self.go_to_main_menu = True
        self.high_score = 0

        self.previous_mouse_position = (0, 0)

        self.menu_selection_sound = pygame.mixer.Sound(self.get_path('menu selection.wav'))
        self.eating_apple = pygame.mixer.Sound(self.get_path('eating apple.wav'))

        self.blank_window = self.create_blank_window()
        self.main_menu_menus = self.create_menus(["PLAY SNAKE", "MAP SIZE", "SNAKE SPEED", "NUMBER OF APPLES", "INFO", "QUIT"], 50, 50, 200, 100, self.MAIN_MENU_TITLE_FONT, self.MENU_OPTIONS_FONT, 0, 5)
        self.map_size_menus = self.create_menus(["MAP SIZES", "10 x 10", "20 x 20", "40 x 40", "BACK TO MAIN MENU"], 50, 50, 300, 100, self.SUB_MENU_TITLE_FONT, self.MENU_OPTIONS_FONT, 1, 4)
        self.snake_speed_menus = self.create_menus(["SNAKE SPEED", "5", "10", "15", "BACK TO MAIN MENU"], 50, 50, 300, 100, self.SUB_MENU_TITLE_FONT, self.MENU_OPTIONS_FONT, 1, 4)
        self.number_of_apples_menus = self.create_menus(["NUMBER OF APPLES", "1", "3", "5", "BACK TO MAIN MENU"], 50, 50, 300, 100, self.SUB_MENU_TITLE_FONT, self.MENU_OPTIONS_FONT, 1, 4)
        self.info_menu = self.create_info_menu()
        self.game_over_menu = self.create_game_over_menu()

        # Game loop
        self.game_loop()

    def game_loop(self):
        clock = pygame.time.Clock()
        while True:
            if self.go_to_main_menu:
                self.display_main_menu()

            self.setup_game()

            while not self.game_over() and not self.go_to_main_menu:
                self.update_snake_position()

                self.display_snake()

                if pygame.key.get_pressed()[pygame.K_k]:
                    clock.tick(self.snake_speed * 2)
                else:
                    clock.tick(self.snake_speed)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.display.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.go_to_main_menu = True
                        elif event.key == pygame.K_ESCAPE:
                            self.game_is_paused()
                        elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.snake_direction != "DOWN":
                            self.snake_direction = "UP"
                        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.snake_direction != "UP":
                            self.snake_direction = "DOWN"
                        elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.snake_direction != "RIGHT":
                            self.snake_direction = "LEFT"
                        elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.snake_direction != "LEFT":
                            self.snake_direction = "RIGHT"

            if not self.go_to_main_menu:
                self.go_to_main_menu = self.display_game_over_menu()
                self.game_is_over = False

    def get_path(self, file_name):
        try:
            return os.path.join(sys._MEIPASS, file_name)
        except AttributeError:
            return 'snake\\resources\\' + file_name

    def setup_game(self):
        self.snake_direction = "RIGHT"
        self.snake_points_x = [self.WINDOW_MID_X, self.WINDOW_MID_X - self.square_size, self.WINDOW_MID_X - self.square_size * 2]
        self.snake_points_y = [self.WINDOW_MID_Y, self.WINDOW_MID_Y, self.WINDOW_MID_Y]
        self.apple_positions = []
        self.apple_positions = self.create_new_apple_positions()
        self.elapsed_time = 0.0
        self.start_time = time.time()
        self.go_to_main_menu = False

    def display_main_menu(self):
        current_selection = 0
        while True:
            current_selection = self.display_menu(self.main_menu_menus, [0, 1, 2, 3, 4, 5], current_selection, [[50, 120], [300, 330], [400, 430], [500, 530], [600, 630], [700, 730]])

            if current_selection == 0:
                return
            elif current_selection == 1:
                self.square_size = self.display_menu(self.map_size_menus, [64, 32, 16, self.square_size], self.square_size, [[400, 430], [500, 530], [600, 630], [700, 730]])
                self.blank_window = self.create_blank_window()
            elif current_selection == 2:
                self.snake_speed = self.display_menu(self.snake_speed_menus, [5, 10, 15, self.snake_speed], self.snake_speed, [[400, 430], [500, 530], [600, 630], [700, 730]])
            elif current_selection == 3:
                self.number_of_apples = self.display_menu(self.number_of_apples_menus, [1, 3, 5, self.number_of_apples], self.number_of_apples, [[400, 430], [500, 530], [600, 630], [700, 730]])
            elif current_selection == 4:
                self.display_menu(self.info_menu, [0], 0, [[700, 730]])
            elif current_selection == 5:
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
                if not pygame.key.get_pressed()[pygame.K_h]:
                    self.window.blit(self.game_over_menu[current_selection], (self.GAME_WINDOW_SIZE / 2 - self.GAME_OVER_WIDTH / 2, self.GAME_WINDOW_SIZE / 2 - self.GAME_OVER_HEIGHT / 2 + self.INFO_HEIGHT))
                    pygame.display.update()
                else:
                    self.display_snake()
            else:
                self.previous_mouse_position = pygame.mouse.get_pos()
                self.window.blit(option_menus[current_selection], (0, 0))
                pygame.display.update()

    def display_game_over_menu(self):
        self.game_is_over = True
        self.elapsed_time += time.time() - self.start_time

        return self.display_menu(self.game_over_menu, [False, True, True], False, [[440, 470], [520, 550]])

    def game_over(self):
        if self.snake_points_x[0] == 0 and self.snake_direction == "LEFT":
            return True
        elif self.snake_points_x[0] == self.GAME_WINDOW_SIZE - self.square_size and self.snake_direction == "RIGHT":
            return True
        elif self.snake_points_y[0] == self.INFO_HEIGHT and self.snake_direction == "UP":
            return True
        elif self.snake_points_y[0] == self.WINDOW_HEIGHT - self.square_size and self.snake_direction == "DOWN":
            return True

        for i in range(1, len(self.snake_points_x)):
            if self.snake_points_x[i] == self.snake_points_x[0] and self.snake_points_y[i] == self.snake_points_y[0]:
                return True

        return False

    def game_is_paused(self):
        self.elapsed_time += time.time() - self.start_time

        colour_step = (self.COLOUR_MAX - self.COLOUR_MIN) / len(self.snake_points_x)
        for i in range(len(self.apple_positions)):
            pygame.draw.rect(self.window, (self.COLOUR_MAX, self.COLOUR_MAX, self.COLOUR_MAX), (self.apple_positions[i][0], self.apple_positions[i][1], self.square_size, self.square_size))
        for i in range(0, len(self.snake_points_x)):
            pygame.draw.rect(self.window, (self.COLOUR_MAX - colour_step * i, self.COLOUR_MAX - colour_step * i, self.COLOUR_MAX - colour_step * i), (self.snake_points_x[i], self.snake_points_y[i], self.square_size, self.square_size))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.go_to_main_menu = True
                        return
                    elif event.key == pygame.K_ESCAPE:
                        self.start_time = time.time()
                        return

    def update_snake_position(self):
        if self.snake_direction == "UP":
            self.snake_points_x.insert(0, self.snake_points_x[0])
            self.snake_points_y.insert(0, self.snake_points_y[0] - self.square_size)
            self.snake_points_x.pop()
            self.snake_points_y.pop()

        elif self.snake_direction == "DOWN":
            self.snake_points_x.insert(0, self.snake_points_x[0])
            self.snake_points_y.insert(0, self.snake_points_y[0] + self.square_size)
            self.snake_points_x.pop()
            self.snake_points_y.pop()

        elif self.snake_direction == "LEFT":
            self.snake_points_x.insert(0, self.snake_points_x[0] - self.square_size)
            self.snake_points_y.insert(0, self.snake_points_y[0])
            self.snake_points_x.pop()
            self.snake_points_y.pop()

        else:  # RIGHT
            self.snake_points_x.insert(0, self.snake_points_x[0] + self.square_size)
            self.snake_points_y.insert(0, self.snake_points_y[0])
            self.snake_points_x.pop()
            self.snake_points_y.pop()

        self.check_for_apple()

    def display_snake(self):
        self.high_score = max(self.high_score, len(self.snake_points_x) - 3)
        colour_step = (self.COLOUR_MAX - self.COLOUR_MIN) / len(self.snake_points_x)

        self.window.blit(self.blank_window, (0, 0))

        current_score_string = self.SNAKE_SCORE_FONT.render(f"Score: {len(self.snake_points_x) - 3}", True, self.TEXT_COLOUR)
        high_score_string = self.SNAKE_FONT.render(f"High Score: {self.high_score}", True, self.TEXT_COLOUR)

        if self.game_is_over:
            elapsed_time_string = self.SNAKE_FONT.render("Time Elapsed: " + time.strftime("%M:%S", time.gmtime(self.elapsed_time)), True, self.TEXT_COLOUR)
        else:
            elapsed_time_string = self.SNAKE_FONT.render("Time Elapsed: " + time.strftime("%M:%S", time.gmtime(time.time() - self.start_time + self.elapsed_time)), True, self.TEXT_COLOUR)

        self.window.blit(current_score_string, (current_score_string.get_rect(center=(self.WINDOW_WIDTH / 2, 25))))
        self.window.blit(high_score_string, (high_score_string.get_rect(center=(self.WINDOW_WIDTH / 2, 65))))
        self.window.blit(elapsed_time_string, (elapsed_time_string.get_rect(center=(self.WINDOW_WIDTH / 2, 100))))

        for pos in self.apple_positions:
            pygame.draw.rect(self.window, (self.COLOUR_MAX, 0, 0), (pos[0], pos[1], self.square_size, self.square_size))

        for i, val in enumerate(zip(self.snake_points_x, self.snake_points_y)):
            pygame.draw.rect(self.window, (0, self.COLOUR_MAX - colour_step * i, 0), (val[0], val[1], self.square_size, self.square_size))

        pygame.display.update()

    def check_for_apple(self):
        for apple in self.apple_positions:
            if self.snake_points_x[0] == apple[0] and self.snake_points_y[0] == apple[1]:
                self.eating_apple.play()
                self.snake_points_x.append(self.snake_points_x[-1])
                self.snake_points_y.append(self.snake_points_y[-1])
                self.apple_positions.pop(self.apple_positions.index(apple))
                self.create_new_apple_positions()

    def create_new_apple_positions(self):
        # If snake so big that there are no positions for an apple -> return
        if len(self.snake_points_x) > (self.GAME_WINDOW_SIZE / self.square_size) * (self.GAME_WINDOW_SIZE / self.square_size) - self.number_of_apples:
            return

        for i in range(self.number_of_apples - len(self.apple_positions)):
            current_apple = [0, 0]
            apple_position_invalid = True
            while apple_position_invalid:
                current_apple[0] = random.randrange(0, self.WINDOW_WIDTH, self.square_size)
                current_apple[1] = random.randrange(self.INFO_HEIGHT, self.WINDOW_HEIGHT, self.square_size)
                apple_position_invalid = False
                for x, y in zip(self.snake_points_x, self.snake_points_y):
                    if current_apple[0] == x and current_apple[1] == y:
                        apple_position_invalid = True
                for an_apple in self.apple_positions:
                    if current_apple[0] == an_apple[0] and current_apple[1] == an_apple[0]:
                        apple_position_invalid = True
            self.apple_positions.append(current_apple)
        return self.apple_positions

    def create_blank_window(self):
        blank_window = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        blank_window.fill(self.WINDOW_BG_DARK)

        draw_light_rect = False
        for y in range(self.INFO_HEIGHT, self.WINDOW_HEIGHT, self.square_size):
            for x in range(0, self.WINDOW_WIDTH, self.square_size):
                if draw_light_rect:
                    pygame.draw.rect(blank_window, self.WINDOW_BG_LIGHT, (x, y, self.square_size, self.square_size))
                draw_light_rect = not draw_light_rect
            draw_light_rect = not draw_light_rect

        pygame.draw.rect(blank_window, self.MENU_WINDOW_BG, (0, 0, self.WINDOW_WIDTH, self.INFO_HEIGHT))

        return blank_window

    def create_menus(self, txt, txt_x, txt_y_title, txt_y_body, txt_y_body_difference, title_font, body_font, selection_start, selection_end):
        fonts = [title_font]
        for i in range(1, len(txt)):
            fonts.append(body_font)

        output = []
        for i in range(selection_start, selection_end + 1):
            temp = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            temp.fill(self.MENU_WINDOW_BG)
            for j in range(len(txt)):
                if j == i:
                    if j == 0:
                        temp.blit(fonts[0].render(txt[0], True, self.SELECTED_TEXT_COLOUR), (txt_x, txt_y_title))
                    else:
                        temp.blit(fonts[j].render(txt[j], True, self.SELECTED_TEXT_COLOUR), (txt_x, txt_y_body + txt_y_body_difference * j))
                else:
                    if j == 0:
                        temp.blit(fonts[0].render(txt[0], True, self.TEXT_COLOUR), (txt_x, txt_y_title))
                    else:
                        temp.blit(fonts[j].render(txt[j], True, self.TEXT_COLOUR), (txt_x, txt_y_body + txt_y_body_difference * j))
            output.append(temp)

        return output

    def create_info_menu(self):
        info_menu = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        info_menu.fill(self.MENU_WINDOW_BG)
        info_menu.blit(self.INFO_MENU_TITLE_FONT.render("INFORMATION", True, self.TEXT_COLOUR), (50, 50))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render("WASD = SNAKE AND MENU NAVIGATION", True, self.TEXT_COLOUR), (50, 150))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render("ARROW KEYS = SNAKE AND MENU NAVIGATION", True, self.TEXT_COLOUR), (50, 200))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render("K = SPEED UP SNAKE", True, self.TEXT_COLOUR), (50, 250))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render("ESC = PAUSE/UNPAUSE GAME", True, self.TEXT_COLOUR), (50, 300))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render("H = HIDE GAME OVER MESSAGE", True, self.TEXT_COLOUR), (50, 350))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render("R = RESTART WHEN GAMER OVER", True, self.TEXT_COLOUR), (50, 400))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render("Q = QUIT TO MAIN MENU WHEN IN GAME", True, self.TEXT_COLOUR), (50, 450))
        info_menu.blit(self.INFO_MENU_BODY_FONT.render("Q = QUIT PROGRAM WHEN IN MAIN MENU", True, self.TEXT_COLOUR), (50, 500))
        info_menu.blit(self.INFO_MENU_RETURN_FONT.render("BACK TO MAIN MENU", True, self.SELECTED_TEXT_COLOUR), (50, 700))

        return [info_menu]

    def create_game_over_menu(self):
        game_over_text = self.GAME_OVER_TITLE_FONT.render("GAME OVER", True, self.TEXT_COLOUR)
        rematch_text_selected = self.GAME_OVER_OPTIONS_FONT.render("REMATCH", True, self.SELECTED_TEXT_COLOUR)
        rematch_text = self.GAME_OVER_OPTIONS_FONT.render("REMATCH", True, self.TEXT_COLOUR)
        quit_text_selected = self.GAME_OVER_OPTIONS_FONT.render("QUIT", True, self.SELECTED_TEXT_COLOUR)
        quit_text = self.GAME_OVER_OPTIONS_FONT.render("QUIT", True, self.TEXT_COLOUR)

        one = pygame.Surface((self.GAME_OVER_WIDTH, self.GAME_OVER_HEIGHT))
        one.fill(self.MENU_WINDOW_BG)
        one.blit(game_over_text, game_over_text.get_rect(center=(self.GAME_OVER_WIDTH / 2, 50)))
        one.blit(rematch_text_selected, rematch_text_selected.get_rect(center=(self.GAME_OVER_WIDTH / 2, self.GAME_OVER_HEIGHT - 115)))
        one.blit(quit_text, quit_text.get_rect(center=(self.GAME_OVER_WIDTH / 2, self.GAME_OVER_HEIGHT - 35)))

        two = pygame.Surface((self.GAME_OVER_WIDTH, self.GAME_OVER_HEIGHT))
        two.fill(self.MENU_WINDOW_BG)
        two.blit(game_over_text, game_over_text.get_rect(center=(self.GAME_OVER_WIDTH / 2, 50)))
        two.blit(rematch_text, rematch_text.get_rect(center=(self.GAME_OVER_WIDTH / 2, self.GAME_OVER_HEIGHT - 115)))
        two.blit(quit_text_selected, quit_text_selected.get_rect(center=(self.GAME_OVER_WIDTH / 2, self.GAME_OVER_HEIGHT - 35)))

        return [one, two]
