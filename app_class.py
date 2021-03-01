import pygame, sys
from settings import *
from random import randint

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

class App:

    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Battle Ships")
        self.running = True
        self.state = 'menu'
        self.battlefield = [[0 for x in range(11)]for x in range(11)]
        self.opponent_battlefield = [[0 for x in range(11)]for x in range(11)]
        self.my_battlefield = [[0 for x in range(11)]for x in range(11)]
        self.previous_battlefield = [[0 for x in range(11)]for x in range(11)]
        self.mouse_position = None
        self.ships_position = []
        self.temporary_ships_position = []
        self.x = 0
        self.y = 0
        self.draw_ship_allow = None
        self.erase_ship_allow = None
        self.player1_battlefield_saved = False
        self.player1_reset = False
        self.player1_reset_occured = False
        self.state_change = True
        self.menu_reset = False
        self.placing_ships_reset = False
        self.reset = False
        roll = randint(0, 1)
        if roll == 1:
            self.player_moved = True
            self.ai_first_move = True
        if roll == 0:
            self.player_moved = False
            self.ai_first_move = False
        self.false_check = False
        self.wait_check = False
        self.game_winner = ""
        self.get_check = False
        self.play_again = False
        self.size1Ships = 0
        self.size2Ships = 0
        self.size3Ships = 0
        self.size4Ships = 0
        pygame.mixer.music.load('bgmusic.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        self.click = pygame.mixer.Sound('click.wav')
        self.click.set_volume(0.2)

    def run(self):
        while self.running:
            if self.state == 'menu':
                self.menu_events()
                self.menu_draw()
            if self.state == 'placing_ships':
                self.placing_ships_events()
                self.placing_ships_draw()
            if self.state == 'play':
                self.play_events()
                self.play_draw()
            if self.state == 'end_screen':
                self.end_screen_events()
                self.end_screen_draw()
        pygame.quit()
        sys.exit()


########################################### menu_events ##########################################

    def menu_events(self):
        if self.reset:
            self.__init__()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_position = pygame.mouse.get_pos()
                self.choose_tile()


    def choose_tile(self):
        for x in range(1,4):
            if x == 1:
                space = 0
            if x == 2:
                space = 0
            if x == 3:
                space = 30
            if self.mouse_position[0] > (screen_width / 2) - (tile_width / 2) and self.mouse_position[0] < ((screen_width / 2) - (tile_width / 2)) + tile_width and self.mouse_position[1] > tiles_y + (x * 100) + space and self.mouse_position[1] < tiles_y + (x * 100) + tile_height + space:
                if x == 1:
                    self.click.play()
                    self.state = 'placing_ships'
                    self.multi = False
                    self.state_change = True
                if x == 2:
                    self.click.play()
                    self.state = 'placing_ships'
                    self.multi = True
                    self.state_change = True
                if x == 3:
                    self.click.play()
                    pygame.time.wait(200)
                    self.running = False


############################################ menu_draw ###########################################

    def menu_draw(self):
        if self.state_change == True and self.menu_reset == False:
            pygame.draw.rect(self.screen, black, (0,0, screen_width, screen_height))
            self.state_change = False
            self.menu_reset = True
        self.write_text(120, "BATTLE SHIPS", green, screen_width / 2, 150)
        self.draw_tiles(self.screen)
        pygame.display.update()


    def draw_tiles(self, screen):
        for x in range(1, 4):
            if x == 1:
                space = 0
                text = "SINGLE PLAYER"
            if x == 2:
                space = 0
                text = "MULTI PLAYER"
            if x == 3:
                space = 30
                text = "QUIT"
            self.write_text(28, text, green, screen_width / 2, tiles_y + 40 + (x * 100) + space)
            pygame.draw.rect(screen, green, ((screen_width / 2) - (tile_width / 2), tiles_y + (x * 100) + space, tile_width, tile_height), 2)

    def write_text(self, size, content, color, x, y):
        font = pygame.font.Font('freesansbold.ttf', size)
        text = font.render(content, True, color, black)
        textRect = text.get_rect()
        textRect.center = (x, y)
        self.screen.blit(text, textRect)


###################################### placing_ships_events ######################################

    def placing_ships_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_position = pygame.mouse.get_pos()
                if self.temporary_ship():
                    self.erase_ship_allow = True
                if self.fieldCheck('player'):
                    self.draw_ship_allow = True
                if self.count_ships():
                    if not self.multi:
                        if self.save_player1_battlefield(): #also go to state: 'play'
                            self.place_opponent_ships()
                    if self.multi:
                        if not self.player1_battlefield_saved:
                            if self.save_player1_battlefield():
                                self.size1Ships = 0
                                self.size2Ships = 0
                                self.size3Ships = 0
                                self.size4Ships = 0
                            continue
                        if self.save_player2_battlefield():
                            self.state_to_play()


    def temporary_ship(self):
        for x in range(10):
            for y in range(10):
                if self.mouse_position[0] > (x * cell_size) + battlefield_x and self.mouse_position[0] < (
                    x * cell_size + cell_size) + battlefield_x and self.mouse_position[1] > (
                    y * cell_size) + battlefield_y and self.mouse_position[1] < (
                    y * cell_size + cell_size) + battlefield_y:
                    if self.battlefield[x][y] == 1:
                        self.battlefield[x][y] = 0
                        self.x = x
                        self.y = y
                        self.click.play()
                        return True
                    else:
                        self.battlefield[x][y] = 1
                        self.x = x
                        self.y = y
                        self.click.play()
                        return False

    def fieldCheck(self, who_called):
        self.temporary_ships_position.clear()
        size1Ships = 0
        size2Ships = 0
        size3Ships = 0
        size4Ships = 0
        breakCheck = 0

        for x in range(10):
            for y in range(10):
                shipSize = 0
                continueCheck = 0
                for match in self.temporary_ships_position:
                    if match == [x, y]:
                        continueCheck = 1
                        break
                if continueCheck == 1:
                    continue
                if self.battlefield[x][y] == 1:
                    shipSize = self.sidesCheck(x, y, 1, 0)
                    if shipSize == 1:
                        size1Ships += 1
                    if shipSize == 2:
                        size2Ships += 1
                    if shipSize == 3:
                        size3Ships += 1
                    if shipSize == 4:
                        size4Ships += 1
                    if shipSize == 5:
                        breakCheck += 1
                        break
            if shipSize == 5:
                breakCheck = 1
                break

        if who_called == 'player':
            if breakCheck == 0:
                self.size1Ships = size1Ships
                self.size2Ships = size2Ships
                self.size3Ships = size3Ships
                self.size4Ships = size4Ships
                return True
            else:
                self.battlefield[self.x][self.y] = 0
                return False

        self.size1Ships = size1Ships
        self.size2Ships = size2Ships
        self.size3Ships = size3Ships
        self.size4Ships = size4Ships
        if who_called == 'opponent':
            if breakCheck == 0 and self.size1Ships <= 4 and self.size2Ships <= 3 and self.size3Ships <= 2 and self.size4Ships <= 1:
                return True
            else:
                self.battlefield[self.x][self.y] = 0
                return False

    def sidesCheck(self, i, j, n, d):
        self.temporary_ships_position.append([i, j])

        if n > 4:
            return 5

        if self.battlefield[i - 1][j - 1] == 1 or \
           self.battlefield[i - 1][j + 1] == 1 or \
           self.battlefield[i + 1][j - 1] == 1 or \
           self.battlefield[i + 1][j + 1] == 1:
            return 5

        if d != 2 and self.battlefield[i - 1][j] == 1:
            n = self.sidesCheck(i - 1, j, n + 1, 1)
        if d != 1 and self.battlefield[i + 1][j] == 1:
            n = self.sidesCheck(i + 1, j, n + 1, 2)
        if d != 4 and self.battlefield[i][j - 1] == 1:
            n = self.sidesCheck(i, j - 1, n + 1, 3)
        if d != 3 and self.battlefield[i][j + 1] == 1:
            n = self.sidesCheck(i, j + 1, n + 1, 4)
        return n

    def count_ships(self):
        ship_count = 0
        for x in range(10):
            for y in range(10):
                if self.battlefield[x][y] == 1:
                    ship_count += 1
        if ship_count == 20 and self.size1Ships == 4 and self.size2Ships == 3 and self.size3Ships == 2 and self.size4Ships == 1:
            return True
        else:
            return False

    def place_opponent_ships(self):
        reset_counter = 0
        while 1 == 1:
            x = randint(0, 9)
            y = randint(0, 9)
            self.battlefield[x][y] = 1
            self.x = x
            self.y = y
            if not self.fieldCheck('opponent'):
                reset_counter += 1
                if reset_counter == 20:
                    for x in range(10):
                        for y in range(10):
                            self.battlefield[x][y] = 0
                    reset_counter = 0
            else:
                reset_counter = 0
            if self.count_ships():
                for x in range(10):
                    for y in range(10):
                        self.opponent_battlefield[x][y] = self.battlefield[x][y]
                        self.battlefield[x][y] = 0
                break

    def save_player1_battlefield(self):
        if self.mouse_position[0] > (screen_width / 2) - (tile_width / 2) and self.mouse_position[0] < (screen_width / 2) - (tile_width / 2) + tile_width and self.mouse_position[1] > 600 and self.mouse_position[1] < 650 + tile_width:
            for x in range(10):
                for y in range(10):
                    self.my_battlefield[x][y] = self.battlefield[x][y]
                    self.battlefield[x][y] = 0
            if self.multi:
                self.player1_battlefield_saved = True
                self.player1_reset = True
            if not self.multi:
                self.state_change = True
                self.state = 'play'
            self.click.play()
            return True

    def save_player2_battlefield(self):
        if self.mouse_position[0] > (screen_width / 2) - (tile_width / 2) and self.mouse_position[0] < (screen_width / 2) - (tile_width / 2) + tile_width and self.mouse_position[1] > 600 and self.mouse_position[1] < 650 + tile_width:
            for x in range(10):
                for y in range(10):
                    self.opponent_battlefield[x][y] = self.battlefield[x][y]
                    self.battlefield[x][y] = 0
            self.click.play()
            return True

    def state_to_play(self):
        self.state_change = True
        self.state = 'play'
        return True


######################################## placing_ships_draw ####################################

    def placing_ships_draw(self):
        if self.state_change == True and self.placing_ships_reset == False:
            pygame.draw.rect(self.screen, black, (0,0, screen_width, screen_height))
            self.state_change = False
            self.placing_ships_reset = True
        if self.player1_reset == True and self.player1_reset_occured == False:
            pygame.draw.rect(self.screen, black, (0, 0, screen_width, screen_height))
            self.player1_reset_occured = True
        self.draw_battlefield(self.screen)
        self.display_play_button(self.screen)
        if self.erase_ship_allow:
            self.erase_ship(self.screen)
        if self.draw_ship_allow:
            self.draw_ship(self.screen)
        self.ship_draw_count(self.screen)
        pygame.display.update()


    def draw_battlefield(self, screen):
        color = green
        pcolor = gray
        if self.player_moved == False:
            color = gray
            pcolor = green
        if self.state == 'placing_ships':
            color = green
        pygame.draw.rect(screen, color, (battlefield_x, battlefield_y, battlefield_width, battlefield_height), 2)
        if self.state == 'play':
            if self.multi:
                self.write_text(40, 'PLAYER 1', pcolor, battlefield_x + (grid_size / 2), 620)
            if not self.multi:
                self.write_text(40, 'PLAYER', pcolor, battlefield_x + (grid_size / 2), 620)
        for x in range(10):
            pygame.draw.line(screen, color, (battlefield_x + (x * cell_size), battlefield_y), (battlefield_x + (x * cell_size), battlefield_y + 500), 2)
            pygame.draw.line(screen, color, (battlefield_x, battlefield_y + (x * cell_size)), (battlefield_x + 500, battlefield_y + (x * cell_size)), 2)

    def draw_ship(self, screen):
        x = self.x
        y = self.y
        if self.battlefield[x][y] == 1:
            pygame.draw.rect(screen, green, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))

    def erase_ship(self, screen):
        x = self.x
        y = self.y
        if self.battlefield[x][y] == 0:
            pygame.draw.rect(screen, black, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))

    def ship_draw_count(self, screen):
        battlefield_x = 800
        battlefield_y = 220
        color = green

        if not self.multi:
            self.write_text(50, 'DEPLOY YOUR SHIPS', color, battlefield_x + 110, battlefield_y - 120)
        if self.multi:
            self.write_text(50, ' PLAYER 1 DEPLOYMENT', color, battlefield_x + 110, battlefield_y - 120)
            if self.player1_battlefield_saved:
                self.write_text(50, ' PLAYER 2 DEPLOYMENT', color, battlefield_x + 110, battlefield_y - 120)

        for y in range(4):
            if y == 0:
                text = str(self.size4Ships) + "/1"
                cells = 4
                if self.size4Ships == 1:
                    color = green
                if self.size4Ships > 1:
                    color = red
                if self.size4Ships < 1:
                    color = gray
            if y == 1:
                text = str(self.size3Ships) + "/2"
                cells = 3
                if self.size3Ships == 2:
                    color = green
                if self.size3Ships > 2:
                    color = red
                if self.size3Ships < 2:
                    color = gray
            if y == 2:
                text = str(self.size2Ships) + "/3"
                cells = 2
                if self.size2Ships == 3:
                    color = green
                if self.size2Ships > 3:
                    color = red
                if self.size2Ships < 3:
                    color = gray
            if y == 3:
                text = str(self.size1Ships) + "/4"
                cells = 1
                if self.size1Ships == 4:
                    color = green
                if self.size1Ships > 4:
                    color = red
                if self.size1Ships < 4:
                    color = gray

            self.write_text(30, text, color, battlefield_x, battlefield_y + (y * cell_size) + 6)
            for x in range(cells):
                pygame.draw.rect(screen, color, ((x * cell_size) + battlefield_x + 30 + 6, (y * cell_size) + battlefield_y - 16, cell_size - 10, cell_size - 10))

    def display_play_button(self, screen):
        color = gray
        if self.multi:
            text = 'DEPLOY'
        if self.multi == False or self.player1_battlefield_saved == True:
            text = 'PLAY'
        if self.count_ships():
            color = green
        pygame.draw.rect(screen, color,((screen_width / 2) - (ps_tile_width / 2), 600, ps_tile_width, tile_height), 2)
        self.write_text(40, text, color, screen_width / 2, 600 + 40)


###################################### play_events ######################################

    def play_events(self):
        if self.get_check:
            pygame.event.get()
            self.get_check = False
        if not self.multi:
            if self.player_moved and not self.ai_first_move:
                for i in range(10):
                    for j in range(10):
                        self.previous_battlefield[i][j] = self.my_battlefield[i][j]
                self.player_moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if not self.multi:
                if self.player_moved and self.ai_first_move:
                    self.ai_first_move = False
                    self.ai_action()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_position = pygame.mouse.get_pos()
                if not self.player_moved:
                    if self.player_action():
                        break
                    if self.multi:
                        continue
                if self.player_moved:
                    if not self.multi:
                        if self.ai_action():
                            break
                    if self.multi:
                        if self.player2_action():
                            break
                self.ai_first_move = False


    def player_action(self):
        cell = self.select_opponent_field()
        if cell == 'hit':
            self.destroy_ship('opponent')
        if cell == 'miss':
            self.mark_cell('opponent')
        if self.win_condition_check(self.opponent_battlefield):
            if not self.multi:
                self.game_winner = 'player'
            if self.multi:
                self.game_winner = 'player1'
            self.state_change = True
            self.state = "end_screen"
            self.wait_check = True
            return True

    def select_opponent_field(self):
        battlefield_x = 730
        for x in range(10):
            for y in range(10):
                if self.mouse_position[0] > (x * cell_size) + battlefield_x and self.mouse_position[0] < (x * cell_size + cell_size) + battlefield_x and self.mouse_position[1] > (y * cell_size) + battlefield_y and self.mouse_position[1] < (y * cell_size + cell_size) + battlefield_y:
                    if self.opponent_battlefield[x][y] == 0:
                        self.player_moved = True
                        self.x = x
                        self.y = y
                        self.click.play()
                        self.wait_check = True
                        return 'miss'
                    if self.opponent_battlefield[x][y] == 1:
                        self.player_moved = False
                        self.x = x
                        self.y = y
                        self.click.play()
                        self.wait_check = True
                        return 'hit'
                    self.click.play()
                    return 'other'

    def player2_action(self):
        cell = self.p2_select_opponent_field()
        if cell == 'hit':
            self.destroy_ship('player')
        if cell == 'miss':
            self.mark_cell('player')
        if self.win_condition_check(self.my_battlefield):
            self.game_winner = 'player2'
            self.state_change = True
            self.state = "end_screen"
            self.wait_check = True
            return True

    def p2_select_opponent_field(self):
        for x in range(10):
            for y in range(10):
                if self.mouse_position[0] > (x * cell_size) + battlefield_x and self.mouse_position[0] < (
                        x * cell_size + cell_size) + battlefield_x and self.mouse_position[1] > (
                        y * cell_size) + battlefield_y and self.mouse_position[1] < (
                        y * cell_size + cell_size) + battlefield_y:
                    if self.my_battlefield[x][y] == 0:
                        self.player_moved = False
                        self.x = x
                        self.y = y
                        self.click.play()
                        self.wait_check = True
                        return 'miss'
                    if self.my_battlefield[x][y] == 1:
                        self.player_moved = True
                        self.x = x
                        self.y = y
                        self.click.play()
                        self.wait_check = True
                        return 'hit'
                    self.click.play()
                    return 'other'

    def ai_action(self):
        cell = self.enemy_shot()
        if cell == 'hit':
            self.destroy_ship('player')
        if cell == 'miss':
            self.mark_cell('player')
        if self.win_condition_check(self.my_battlefield):
            self.game_winner = 'player_lost'
            self.state_change = True
            self.state = "end_screen"
            self.wait_check = True
            return True
        self.wait_check = True

    def enemy_shot(self):
        #self.player_moved = False
        shot_fired = False
        while not shot_fired:

            for i in range(10):
                for j in range(10):
                    if self.my_battlefield[i][j] == 2:
                        check = True
                        dir0 = True
                        dir1 = True
                        dir2 = True
                        dir3 = True
                        while check:
                            dir = randint(0, 4)

                            if dir == 0:
                                if i != 0:
                                    x = i - 1
                                    y = j
                                    shot = self.check_cell(x, y)
                                    if shot == 'hit':
                                        return 'hit'
                                    if shot == 'miss':
                                        return 'miss'
                                    if shot == 'wrong_cell':
                                        dir0 = False
                                else:
                                    dir0 = False

                            if dir == 1:
                                if i != 9:
                                    x = i + 1
                                    y = j
                                    shot = self.check_cell(x, y)
                                    if shot == 'hit':
                                        return 'hit'
                                    if shot == 'miss':
                                        return 'miss'
                                    if shot == 'wrong_cell':
                                        dir1 = False
                                else:
                                    dir1 = False

                            if dir == 2:
                                if j != 0:
                                    x = i
                                    y = j - 1
                                    shot = self.check_cell(x, y)
                                    if shot == 'hit':
                                        return 'hit'
                                    if shot == 'miss':
                                        return 'miss'
                                    if shot == 'wrong_cell':
                                        dir2 = False
                                else:
                                    dir2 = False

                            if dir == 3:
                                if j != 9:
                                    x = i
                                    y = j + 1
                                    shot = self.check_cell(x, y)
                                    if shot == 'hit':
                                        return 'hit'
                                    if shot == 'miss':
                                        return 'miss'
                                    if shot == 'wrong_cell':
                                        dir3 = False
                                else:
                                    dir3 = False

                            if dir0 == False and dir1 == False and dir2 == False and dir3 == False:
                                check = False

            x = randint(0, 9)
            y = randint(0, 9)

            shot = self.check_cell(x, y)
            if shot == 'hit':
                return 'hit'
            if shot == 'miss':
                return 'miss'

    def check_cell(self, x, y):
        if self.my_battlefield[x][y] == 1:
            self.x = x
            self.y = y
            return 'hit'

        if self.my_battlefield[x - 1][y - 1] != 3 and self.my_battlefield[x - 1][y + 1] != 3 and self.my_battlefield[x + 1][y - 1] != 3 and self.my_battlefield[x + 1][y + 1] != 3 and self.my_battlefield[x][y - 1] != 3 and self.my_battlefield[x][y + 1] != 3 and self.my_battlefield[x - 1][y] != 3 and self.my_battlefield[x + 1][y] != 3:
            if self.my_battlefield[x - 1][ y - 1] != 2 and self.my_battlefield[x - 1][ y + 1] != 2 and self.my_battlefield[x + 1][ y - 1] != 2 and self.my_battlefield[x + 1][ y + 1] != 2:
                if self.my_battlefield[x][y] == 0:
                    self.x = x
                    self.y = y
                    return 'miss'

        return 'wrong_cell'

    def mark_cell(self, target):
        if target == 'opponent':
            self.opponent_battlefield[self.x][self.y] = 5
        if target == 'player':
            self.my_battlefield[self.x][self.y] = 5

    def destroy_ship(self, target):
        if target == 'opponent':
            self.ships_position.clear()
            self.false_check = False
            if self.check_sides(self.opponent_battlefield, self.x, self.y, 0, 1):
                for pos in self.ships_position:
                    self.opponent_battlefield[pos[0]][pos[1]] = 3
            else:
                self.opponent_battlefield[self.ships_position[0][0]][self.ships_position[0][1]] = 2
        if target == 'player':
            self.ships_position.clear()
            self.false_check = False
            if self.check_sides(self.my_battlefield, self.x, self.y, 0, 1):
                for pos in self.ships_position:
                    self.my_battlefield[pos[0]][pos[1]] = 3
            else:
                self.my_battlefield[self.ships_position[0][0]][self.ships_position[0][1]] = 2

    def check_sides(self, field, x, y, d, n):
        self.ships_position.append([x, y])

        if (d == 1 or d == 0) and field[x][y - 1] == 1:
            self.false_check = True
            return False

        if (d == 2 or d == 0) and field[x][y + 1] == 1:
            self.false_check = True
            return False

        if (d == 3 or d == 0) and field[x - 1][y] == 1:
            self.false_check = True
            return False

        if (d == 4 or d == 0) and field[x + 1][y] == 1:
            self.false_check = True
            return False

        if (d == 1 or d == 0) and field[x][y - 1] == 2:
            self.check_sides(field, x, y - 1, 1, n + 1)

        if (d == 2 or d == 0) and field[x][y + 1] == 2:
            self.check_sides(field, x, y + 1, 2, n + 1)

        if (d == 3 or d == 0) and field[x - 1][y] == 2:
            self.check_sides(field, x - 1, y, 3, n + 1)

        if (d == 4 or d == 0) and field[x + 1][y] == 2:
            self.check_sides(field, x + 1, y, 4, n + 1)

        if self.false_check:
            return False
        else:
            return True

    def win_condition_check(self, field):
        for x in range(10):
            for y in range(10):
                if field[x][y] == 1:
                    return False
        return True


####################################### play_draw #######################################

    def play_draw(self):
        if self.state_change == True and self.state == 'play':
            pygame.draw.rect(self.screen, black, (0,0, screen_width, screen_height))
            self.draw_battlefield(self.screen)
            self.display_ships(self.screen)
            self.draw_opponent_battlefield(self.screen)
            self.display_opponent_ships(self.screen)
            self.state_change = False
        if self.multi == True and self.wait_check == True:
            self.display_ships_mp(self.screen)
            self.display_opponent_ships_mp((self.screen))
            pygame.display.update()
            pygame.time.wait(500)
            self.wait_check = False
            self.get_check = True
        if not self.multi:
            self.display_opponent_ships2(self.screen)
            pygame.display.update()
            if self.wait_check == True:
                pygame.time.wait(500)
            self.display_ships2(self.screen)
        self.draw_battlefield(self.screen)
        self.draw_opponent_battlefield(self.screen)
        if self.multi:
            self.display_ships(self.screen)
        self.display_opponent_ships(self.screen)
        if self.game_winner == 'player' and self.state == 'end_screen':
            pygame.time.wait(250)
            return False
        pygame.display.update()
        if self.wait_check == True:
            pygame.time.wait(500)
        self.display_ships(self.screen)
        pygame.display.update()
        if self.wait_check == True:
            pygame.time.wait(500)
            self.wait_check = False
            self.get_check = True
        if self.game_winner == 'player_lost':
            pygame.time.wait(250)


    def draw_opponent_battlefield(self, screen):
        battlefield_x = 730
        color = green
        pcolor = gray
        if self.player_moved:
            color = gray
            pcolor = green
        pygame.draw.rect(screen, color, (battlefield_x, battlefield_y, battlefield_width, battlefield_height), 2)
        if self.state == 'play':
            if self.multi:
                self.write_text(40, 'PLAYER 2', pcolor, battlefield_x + (grid_size / 2), 620)
            if not self.multi:
                self.write_text(40, 'OPPONENT', pcolor, battlefield_x + (grid_size / 2), 620)
        for x in range(10):
            pygame.draw.line(screen, color, (battlefield_x + (x * cell_size), battlefield_y), (battlefield_x + (x * cell_size), battlefield_y + 500), 2)
            pygame.draw.line(screen, color, (battlefield_x, battlefield_y + (x * cell_size)), (battlefield_x + 500, battlefield_y + (x * cell_size)), 2)

    def display_ships(self, screen):
        ccolor = green
        if self.player_moved == False:
            ccolor = gray
        for x in range(10):
            for y in range(10):
                if not self.multi:
                    if self.my_battlefield[x][y] == 1:
                        pygame.draw.rect(screen, green, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10,cell_size - 10))
                if self.my_battlefield[x][y] == 2:
                    pygame.draw.rect(screen, orange, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)
                if self.my_battlefield[x][y] == 3:
                    pygame.draw.rect(screen, red, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)
                if self.my_battlefield[x][y] == 5:
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)

    def display_ships_mp(self, screen):
        ccolor = gray
        if self.player_moved == False:
            ccolor = green

        for x in range(10):
            for y in range(10):
                if not self.multi:
                    if self.my_battlefield[x][y] == 1:
                        pygame.draw.rect(screen, green, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10,cell_size - 10))
                if self.my_battlefield[x][y] == 2:
                    pygame.draw.rect(screen, orange, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)
                if self.my_battlefield[x][y] == 3:
                    pygame.draw.rect(screen, red, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)
                if self.my_battlefield[x][y] == 5:
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)

    def display_ships2(self, screen):
        ccolor = green
        if self.player_moved == False:
            ccolor = gray
        for x in range(10):
            for y in range(10):
                if self.previous_battlefield[x][y] == 1:
                     pygame.draw.rect(screen, green, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10,cell_size - 10))
                if self.previous_battlefield[x][y] == 2:
                    pygame.draw.rect(screen, orange, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)
                if self.previous_battlefield[x][y] == 3:
                    pygame.draw.rect(screen, red, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)
                if self.previous_battlefield[x][y] == 5:
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)

    def display_opponent_ships(self, screen):
        battlefield_x = 730
        ccolor = green
        if self.player_moved:
            ccolor = gray
        for x in range(10):
            for y in range(10):
                #if self.opponent_battlefield[x][y] == 1:
                 #   pygame.draw.rect(screen, green, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                if self.opponent_battlefield[x][y] == 2:
                    color = orange
                    pygame.draw.rect(screen, color, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)
                if self.opponent_battlefield[x][y] == 3:
                    color = red
                    pygame.draw.rect(screen, color, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)
                if self.opponent_battlefield[x][y] == 5:
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)

    def display_opponent_ships_mp(self, screen):
        battlefield_x = 730
        ccolor = gray
        if self.player_moved:
            ccolor = green
        for x in range(10):
            for y in range(10):
                #if self.opponent_battlefield[x][y] == 1:
                 #   pygame.draw.rect(screen, green, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                if self.opponent_battlefield[x][y] == 2:
                    color = orange
                    pygame.draw.rect(screen, color, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)
                if self.opponent_battlefield[x][y] == 3:
                    color = red
                    pygame.draw.rect(screen, color, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)
                if self.opponent_battlefield[x][y] == 5:
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)

    def display_opponent_ships2(self, screen):
        battlefield_x = 730
        ccolor = green
        for x in range(10):
            for y in range(10):
                #if self.opponent_battlefield[x][y] == 1:
                 #   pygame.draw.rect(screen, green, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                if self.opponent_battlefield[x][y] == 2:
                    color = orange
                    pygame.draw.rect(screen, color, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)
                if self.opponent_battlefield[x][y] == 3:
                    color = red
                    pygame.draw.rect(screen, color, ((x * cell_size) + battlefield_x + 6, (y * cell_size) + battlefield_y + 6, cell_size - 10, cell_size - 10))
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)
                if self.opponent_battlefield[x][y] == 5:
                    self.draw_cross(self.screen, ccolor, x, y, battlefield_x)

    def draw_cross(self, screen, color, x, y, battlefield_x):
        pygame.draw.line(screen, color, ((x * cell_size) + battlefield_x + 10, (y * cell_size) + battlefield_y + 10), ((x * cell_size) + battlefield_x - 10 + cell_size, (y * cell_size) + battlefield_y - 10 + cell_size), 2)
        pygame.draw.line(screen, color, ((x * cell_size) + battlefield_x + 10, (y * cell_size) + battlefield_y - 10 + cell_size), ((x * cell_size) + battlefield_x - 10 + cell_size, (y * cell_size) + battlefield_y + 10), 2)


###################################### end_screen_events ######################################

    def end_screen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_position = pygame.mouse.get_pos()
                self.choose_end_screen_tile()


    def choose_end_screen_tile(self):
        for x in range(1,3):
            if x == 1:
                space = 0
            if x == 2:
                space = 30

            if self.mouse_position[0] > (screen_width / 2) - (tile_width / 2) and self.mouse_position[0] < ((screen_width / 2) - (tile_width / 2)) + tile_width and self.mouse_position[1] > tiles_y + (x * 100) + space and self.mouse_position[1] < tiles_y + (x * 100) + tile_height + space:
                if x == 1:
                    self.click.play()
                    self.reset = True
                    self.state = 'menu'
                    self.state_change = True
                if x == 2:
                    self.click.play()
                    pygame.time.wait(200)
                    self.running = False


###################################### end_screen_draw ######################################

    def end_screen_draw(self):
        pygame.draw.rect(self.screen, black, (0, 0, screen_width, screen_height))
        self.draw_end_screen_tiles(self.screen)
        self.display_text()
        pygame.display.update()


    def draw_end_screen_tiles(self, screen):
        for x in range(1, 3):
            if x == 1:
                space = 0
                text = "MAIN MENU"
                self.play_again = True
            if x == 2:
                space = 30
                text = "QUIT"
            self.write_text(28, text, green, screen_width / 2, tiles_y + 40 + (x * 100) + space)
            pygame.draw.rect(screen, green, ((screen_width / 2) - (tile_width / 2), tiles_y + (x * 100) + space, tile_width, tile_height), 2)

    def display_text(self):
        if self.game_winner == 'player':
            text = "YOU WON"
            color = green
        if self.game_winner == 'player1':
            text = "PLAYER 1 WON"
            color = green
        if self.game_winner == 'player2':
            text = "PLAYER 2 WON"
            color = green
        if self.game_winner == 'player_lost':
            text = "YOU LOST"
            color = red
        self.write_text(80, text, color, screen_width / 2, 150)
