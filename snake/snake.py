import os
import sys
import time
import random
import pygame


class App:
    def __init__(self):
        self.window_size = 640
        self.info_height = 128
        self.window_width = self.window_size
        self.window_height = self.window_size + self.info_height
        self.window_mid_x = int(self.window_width / 2)
        self.window_mid_y = int((self.window_height - self.info_height) / 2) + self.info_height

        pygame.init()
        pygame.display.set_caption("Snake")
        pygame.display.set_icon(pygame.image.load(self.get_path("app.ico")))
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

        self.game_over_width = 350
        self.game_over_height = 250

        self.window_bg_dark = (16, 16, 16)
        self.window_bg_light = (24, 24, 24)
        self.menu_window_bg = (8, 8, 8)

        self.text_colour = (255, 255, 255)
        self.selected_text_colour = (0, 128, 156)

        self.colour_min = 32
        self.colour_max = 196

        self.main_font = "Video Game Font"
        self.main_menu_title_font = pygame.font.SysFont(self.main_font, 110)
        self.sub_menu_title_font = pygame.font.SysFont(self.main_font, 72)
        self.menu_options_font = pygame.font.SysFont(self.main_font, 48)

        self.info_menu_title_font = pygame.font.SysFont(self.main_font, 72)
        self.info_menu_body_font = pygame.font.SysFont(self.main_font, 32)
        self.info_menu_return_font = pygame.font.SysFont(self.main_font, 48)

        self.game_over_title_font = pygame.font.SysFont(self.main_font, 72)
        self.game_over_options_font = pygame.font.SysFont(self.main_font, 48)

        self.snake_score_font = pygame.font.SysFont(self.main_font, 48)
        self.snake_font = pygame.font.SysFont(self.main_font, 32)

        self.square_size = 32
        self.snake_speed = 10
        self.number_of_apples = 3
        self.high_score = 0

        self.previous_mouse_position = (0, 0)

        self.blank_window = self.create_blank_window()
        self.main_menus = self.create_menus(["PLAY SNAKE", "MAP SIZE", "SNAKE SPEED", "NUMBER OF APPLES", "INFO", "QUIT"],
                                            50, 50, 200, 100, self.main_menu_title_font, self.menu_options_font, 0, 5)
        self.map_size_menus = self.create_menus(["MAP SIZES", "10 x 10", "20 x 20", "40 x 40", "BACK TO MAIN MENU"],
                                                50, 50, 300, 100, self.sub_menu_title_font, self.menu_options_font, 1, 4)
        self.snake_speed_menus = self.create_menus(["SNAKE SPEED", "5", "10", "15", "BACK TO MAIN MENU"],
                                                   50, 50, 300, 100, self.sub_menu_title_font, self.menu_options_font, 1, 4)
        self.apple_amount_menus = self.create_menus(["NUMBER OF APPLES", "1", "3", "5", "BACK TO MAIN MENU"],
                                                    50, 50, 300, 100, self.sub_menu_title_font, self.menu_options_font, 1, 4)
        self.info_menu = self.create_info_menu()
        self.game_over_menu = self.create_game_over_menu()

        self.go_to_main_menu = True
        while True:
            if self.go_to_main_menu:
                self.display_main_menu()

            self.snake_direction = "RIGHT"
            self.points_x = [self.window_mid_x, self.window_mid_x - self.square_size, self.window_mid_x - self.square_size * 2]
            self.points_y = [self.window_mid_y, self.window_mid_y, self.window_mid_y]
            self.apple_positions = []
            self.apple_positions = self.create_new_apple_positions()
            self.elapsed_time = 0.0
            self.start_time = time.time()
            self.game_is_over = False

            self.go_immediately_to_main_menu = False
            while not self.game_over() and not self.go_immediately_to_main_menu:
                self.update_snake_position()

                self.display_snake()

                if pygame.key.get_pressed()[pygame.K_k]:
                    self.clock.tick(self.snake_speed * 2)
                else:
                    self.clock.tick(self.snake_speed)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.display.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.go_immediately_to_main_menu = True
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

            if not self.go_immediately_to_main_menu:
                self.go_to_main_menu = self.display_game_over_menu()

    # noinspection PyMethodMayBeStatic
    def get_path(self, file_name):
        try:
            # noinspection PyProtectedMember
            return os.path.join(sys._MEIPASS, file_name)
        except AttributeError:
            return "snake\\resources\\" + file_name

    def create_blank_window(self):
        blank_window = pygame.Surface((self.window_width, self.window_height))
        blank_window.fill(self.window_bg_dark)

        draw_light_rect = False
        for y in range(self.info_height, self.window_height, self.square_size):
            for x in range(0, self.window_width, self.square_size):
                if draw_light_rect:
                    pygame.draw.rect(blank_window, self.window_bg_light, (x, y, self.square_size, self.square_size))
                draw_light_rect = not draw_light_rect
            draw_light_rect = not draw_light_rect

        pygame.draw.rect(blank_window, self.menu_window_bg, (0, 0, self.window_width, self.info_height))

        return blank_window

    def create_menus(self, txt, txt_x, txt_y_title, txt_y_body, txt_y_body_difference, title_font, body_font, selection_start, selection_end):
        fonts = [title_font]
        for i in range(1, len(txt)):
            fonts.append(body_font)

        output = []
        for i in range(selection_start, selection_end + 1):
            temp = pygame.Surface((self.window_width, self.window_height))
            temp.fill(self.menu_window_bg)
            for j in range(len(txt)):
                if j == i:
                    if j == 0:
                        temp.blit(fonts[0].render(txt[0], True, self.selected_text_colour), (txt_x, txt_y_title))
                    else:
                        temp.blit(fonts[j].render(txt[j], True, self.selected_text_colour), (txt_x, txt_y_body + txt_y_body_difference * j))
                else:
                    if j == 0:
                        temp.blit(fonts[0].render(txt[0], True, self.text_colour), (txt_x, txt_y_title))
                    else:
                        temp.blit(fonts[j].render(txt[j], True, self.text_colour), (txt_x, txt_y_body + txt_y_body_difference * j))
            output.append(temp)

        return output

    def create_info_menu(self):
        info_menu = pygame.Surface((self.window_width, self.window_height))
        info_menu.fill(self.menu_window_bg)
        info_menu.blit(self.info_menu_title_font.render("INFORMATION", True, self.text_colour), (50, 50))
        info_menu.blit(self.info_menu_body_font.render("WASD = SNAKE AND MENU NAVIGATION", True, self.text_colour), (50, 150))
        info_menu.blit(self.info_menu_body_font.render("ARROW KEYS = SNAKE AND MENU NAVIGATION", True, self.text_colour), (50, 200))
        info_menu.blit(self.info_menu_body_font.render("K = SPEED UP SNAKE", True, self.text_colour), (50, 250))
        info_menu.blit(self.info_menu_body_font.render("ESC = PAUSE/UNPAUSE GAME", True, self.text_colour), (50, 300))
        info_menu.blit(self.info_menu_body_font.render("H = HIDE GAME OVER MESSAGE", True, self.text_colour), (50, 350))
        info_menu.blit(self.info_menu_body_font.render("R = RESTART WHEN GAMER OVER", True, self.text_colour), (50, 400))
        info_menu.blit(self.info_menu_body_font.render("Q = QUIT TO MAIN MENU WHEN IN GAME", True, self.text_colour), (50, 450))
        info_menu.blit(self.info_menu_body_font.render("Q = QUIT PROGRAM WHEN IN MAIN MENU", True, self.text_colour), (50, 500))
        info_menu.blit(self.info_menu_return_font.render("BACK TO MAIN MENU", True, self.selected_text_colour), (50, 700))

        return info_menu

    def create_game_over_menu(self):
        game_over_text = self.game_over_title_font.render("GAME OVER", True, self.text_colour)
        rematch_text_selected = self.game_over_options_font.render("REMATCH", True, self.selected_text_colour)
        rematch_text = self.game_over_options_font.render("REMATCH", True, self.text_colour)
        quit_text_selected = self.game_over_options_font.render("QUIT", True, self.selected_text_colour)
        quit_text = self.game_over_options_font.render("QUIT", True, self.text_colour)

        one = pygame.Surface((self.game_over_width, self.game_over_height))
        one.fill(self.menu_window_bg)
        one.blit(game_over_text, game_over_text.get_rect(center=(self.game_over_width / 2, 50)))
        one.blit(rematch_text_selected, rematch_text_selected.get_rect(center=(self.game_over_width / 2, self.game_over_height - 115)))
        one.blit(quit_text, quit_text.get_rect(center=(self.game_over_width / 2, self.game_over_height - 35)))

        two = pygame.Surface((self.game_over_width, self.game_over_height))
        two.fill(self.menu_window_bg)
        two.blit(game_over_text, game_over_text.get_rect(center=(self.game_over_width / 2, 50)))
        two.blit(rematch_text, rematch_text.get_rect(center=(self.game_over_width / 2, self.game_over_height - 115)))
        two.blit(quit_text_selected, quit_text_selected.get_rect(center=(self.game_over_width / 2, self.game_over_height - 35)))

        return [one, two]

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
                            current_selection = 5
                        else:
                            current_selection -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if current_selection == 5:
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
                    elif 300 <= y <= 330:
                        current_selection = 1
                    elif 400 <= y <= 430:
                        current_selection = 2
                    elif 500 <= y <= 530:
                        current_selection = 3
                    elif 600 <= y <= 630:
                        current_selection = 4
                    elif 700 <= y <= 730:
                        current_selection = 5

                if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    if current_selection == 0:
                        return
                    elif current_selection == 1:
                        self.display_map_size_options_menu()
                    elif current_selection == 2:
                        self.display_snake_speed_options_menu()
                    elif current_selection == 3:
                        self.display_apple_amount_options_menu()
                    elif current_selection == 4:
                        self.display_info_menu()
                    elif current_selection == 5:
                        pygame.display.quit()
                        sys.exit()

            self.previous_mouse_position = pygame.mouse.get_pos()

            self.window.blit(self.main_menus[current_selection], (0, 0))

            pygame.display.update()

    def display_map_size_options_menu(self):
        if self.square_size == 64:
            current_selection = 0
        elif self.square_size == 32:
            current_selection = 1
        else:  # self.square_size == 16:
            current_selection = 2
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
                    elif event.key == pygame.K_q:
                        return

                _, y = pygame.mouse.get_pos()

                if self.previous_mouse_position != pygame.mouse.get_pos():
                    if 400 <= y <= 430:
                        current_selection = 0
                    elif 500 <= y <= 530:
                        current_selection = 1
                    elif 600 <= y <= 630:
                        current_selection = 2
                    elif 700 <= y <= 730:
                        current_selection = 3

                if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    if current_selection == 0:
                        self.square_size = 64
                    elif current_selection == 1:
                        self.square_size = 32
                    elif current_selection == 2:
                        self.square_size = 16
                    elif current_selection == 3:
                        pass
                    self.blank_window = self.create_blank_window()
                    return

            self.previous_mouse_position = pygame.mouse.get_pos()

            self.window.blit(self.map_size_menus[current_selection], (0, 0))

            pygame.display.update()

    def display_snake_speed_options_menu(self):
        if self.snake_speed == 5:
            current_selection = 0
        elif self.snake_speed == 10:
            current_selection = 1
        else:  # self.snake_speed == 15:
            current_selection = 2
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
                    elif event.key == pygame.K_q:
                        return

                _, y = pygame.mouse.get_pos()

                if self.previous_mouse_position != pygame.mouse.get_pos():
                    if 400 <= y <= 430:
                        current_selection = 0
                    elif 500 <= y <= 530:
                        current_selection = 1
                    elif 600 <= y <= 630:
                        current_selection = 2
                    elif 700 <= y <= 730:
                        current_selection = 3

                if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    if current_selection == 0:
                        self.snake_speed = 5
                    elif current_selection == 1:
                        self.snake_speed = 10
                    elif current_selection == 2:
                        self.snake_speed = 15
                    elif current_selection == 3:
                        return
                    self.blank_window = self.create_blank_window()
                    return

            self.previous_mouse_position = pygame.mouse.get_pos()

            self.window.blit(self.snake_speed_menus[current_selection], (0, 0))

            pygame.display.update()

    def display_apple_amount_options_menu(self):
        if self.number_of_apples == 1:
            current_selection = 0
        elif self.number_of_apples == 3:
            current_selection = 1
        else:  # self.number_of_apples == 5:
            current_selection = 2
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
                    elif event.key == pygame.K_q:
                        return

                _, y = pygame.mouse.get_pos()

                if self.previous_mouse_position != pygame.mouse.get_pos():
                    if 400 <= y <= 430:
                        current_selection = 0
                    elif 500 <= y <= 530:
                        current_selection = 1
                    elif 600 <= y <= 630:
                        current_selection = 2
                    elif 700 <= y <= 730:
                        current_selection = 3

                if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    if current_selection == 0:
                        self.number_of_apples = 1
                    elif current_selection == 1:
                        self.number_of_apples = 3
                    elif current_selection == 2:
                        self.number_of_apples = 5
                    return

            self.previous_mouse_position = pygame.mouse.get_pos()

            self.window.blit(self.apple_amount_menus[current_selection], (0, 0))

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
                    if 700 <= y <= 730:
                        return

            pygame.display.update()

    def display_game_over_menu(self):
        self.game_is_over = True
        self.elapsed_time += time.time() - self.start_time
        current_selection = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return False
                    elif event.key == pygame.K_q:
                        return True
                    elif event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if current_selection == 0:
                            current_selection = 1
                        else:
                            current_selection = 0

                _, y = pygame.mouse.get_pos()

                if self.previous_mouse_position != pygame.mouse.get_pos():
                    if 440 <= y <= 470:
                        current_selection = 0
                    elif 520 <= y <= 550:
                        current_selection = 1

                if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    if current_selection == 0:
                        return False
                    elif current_selection == 1:
                        return True

            self.previous_mouse_position = pygame.mouse.get_pos()

            if not pygame.key.get_pressed()[pygame.K_h]:
                self.window.blit(self.game_over_menu[current_selection], (self.window_size / 2 - self.game_over_width / 2,
                                                                          self.window_size / 2 - self.game_over_height / 2 + self.info_height))
                pygame.display.update()
            else:
                self.display_snake()

    def game_over(self):
        if self.points_x[0] == 0 and self.snake_direction == "LEFT":
            return True
        elif self.points_x[0] == self.window_size - self.square_size and self.snake_direction == "RIGHT":
            return True
        elif self.points_y[0] == self.info_height and self.snake_direction == "UP":
            return True
        elif self.points_y[0] == self.window_height - self.square_size and self.snake_direction == "DOWN":
            return True

        for i in range(1, len(self.points_x)):
            if self.points_x[i] == self.points_x[0] and self.points_y[i] == self.points_y[0]:
                return True

        return False

    def game_is_paused(self):
        self.elapsed_time += time.time() - self.start_time

        colourStep = (self.colour_max - self.colour_min) / len(self.points_x)
        for i in range(len(self.apple_positions)):
            pygame.draw.rect(self.window, (self.colour_max, self.colour_max, self.colour_max),
                             (self.apple_positions[i][0], self.apple_positions[i][1], self.square_size, self.square_size))
        for i in range(0, len(self.points_x)):
            pygame.draw.rect(self.window, (self.colour_max - colourStep * i, self.colour_max - colourStep * i, self.colour_max - colourStep * i),
                             (self.points_x[i], self.points_y[i], self.square_size, self.square_size))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.go_immediately_to_main_menu = True
                        return
                    elif event.key == pygame.K_ESCAPE:
                        self.start_time = time.time()
                        return

    def display_snake(self):
        self.high_score = max(self.high_score, len(self.points_x) - 3)
        colour_step = (self.colour_max - self.colour_min) / len(self.points_x)

        self.window.blit(self.blank_window, (0, 0))

        current_score_string = self.snake_score_font.render(f"Score: {len(self.points_x) - 3}", True, self.text_colour)
        high_score_string = self.snake_font.render(f"High Score: {self.high_score}", True, self.text_colour)

        if self.game_is_over:
            elapsed_time_string = self.snake_font.render("Time Elapsed: " + time.strftime("%M:%S", time.gmtime(self.elapsed_time)),
                                                         True, self.text_colour)
        else:
            elapsed_time_string = self.snake_font.render("Time Elapsed: " +
                                                         time.strftime("%M:%S", time.gmtime(time.time() - self.start_time + self.elapsed_time)),
                                                         True, self.text_colour)

        self.window.blit(current_score_string, (current_score_string.get_rect(center=(self.window_width / 2, 25))))
        self.window.blit(high_score_string, (high_score_string.get_rect(center=(self.window_width / 2, 65))))
        self.window.blit(elapsed_time_string, (elapsed_time_string.get_rect(center=(self.window_width / 2, 100))))

        for i in range(len(self.apple_positions)):
            pygame.draw.rect(self.window, (self.colour_max, 0, 0),
                             (self.apple_positions[i][0], self.apple_positions[i][1], self.square_size, self.square_size))

        for i in range(len(self.points_x)):
            pygame.draw.rect(self.window, (0, self.colour_max - colour_step * i, 0),
                             (self.points_x[i], self.points_y[i], self.square_size, self.square_size))

        pygame.display.update()

    def update_snake_position(self):
        if self.snake_direction == "UP":
            self.points_x.insert(0, self.points_x[0])
            self.points_y.insert(0, self.points_y[0] - self.square_size)
            self.points_x.pop()
            self.points_y.pop()

        elif self.snake_direction == "DOWN":
            self.points_x.insert(0, self.points_x[0])
            self.points_y.insert(0, self.points_y[0] + self.square_size)
            self.points_x.pop()
            self.points_y.pop()

        elif self.snake_direction == "LEFT":
            self.points_x.insert(0, self.points_x[0] - self.square_size)
            self.points_y.insert(0, self.points_y[0])
            self.points_x.pop()
            self.points_y.pop()

        else:  # RIGHT
            self.points_x.insert(0, self.points_x[0] + self.square_size)
            self.points_y.insert(0, self.points_y[0])
            self.points_x.pop()
            self.points_y.pop()

        self.check_for_apple()

    def check_for_apple(self):
        for an_apple in self.apple_positions:
            if self.points_x[0] == an_apple[0] and self.points_y[0] == an_apple[1]:
                self.points_x.append(self.points_x[-1])
                self.points_y.append(self.points_y[-1])
                self.apple_positions.pop(self.apple_positions.index(an_apple))
                self.create_new_apple_positions()

    def create_new_apple_positions(self):
        # If snake so big that there are no positions for an apple then return
        if len(self.points_x) > (self.window_size / self.square_size) * (self.window_size / self.square_size) - self.number_of_apples:
            return

        for i in range(self.number_of_apples - len(self.apple_positions)):
            current_apple = [0, 0]
            apple_position_invalid = True
            while apple_position_invalid:
                current_apple[0] = random.randrange(0, self.window_width, self.square_size)
                current_apple[1] = random.randrange(self.info_height, self.window_height, self.square_size)
                apple_position_invalid = False
                for x, y in zip(self.points_x, self.points_y):
                    if current_apple[0] == x and current_apple[1] == y:
                        apple_position_invalid = True
                for an_apple in self.apple_positions:
                    if current_apple[0] == an_apple[0] and current_apple[1] == an_apple[0]:
                        apple_position_invalid = True
            self.apple_positions.append(current_apple)
        return self.apple_positions
