import pygame
import sys
import numpy as np
import LinkedList
import openpyxl

# constants
SCREEN_SIZE = 1000, 700
MAP_SIZE = 800, 600
ROAD_WIDTH = 55
MAP_POINT = 0, 100
STARTING_POINT = -ROAD_WIDTH, 545
STARTING_POINT_CENTER = STARTING_POINT[0] + int(ROAD_WIDTH/2), STARTING_POINT[1] + int(ROAD_WIDTH/2)
ICON_SIZE = (65, 65)
MAXFPS = 50

# colors,,kki
INTERFACE, MSG, ICON = 0, 1, 2

# button classifier
MK_TOWER, MK_STAR, UPGRADE, PP = 0, 1, 2, 3

COLORS = [
    (int(0xCC), int(0xCC), int(0xCC)),
    (0, 0, 0),
    (int(0x55), int(0x55), int(0x55))
]

# workbook
wb = openpyxl.load_workbook('data.xlsx')
ws = wb.get_sheet_by_name("balloon")

TOWERS = LinkedList.LL()
BALLOONS = LinkedList.LL()
DARTS = LinkedList.LL()
BUTTON =[]

map_img = pygame.image.load("map1.png")
map_img = pygame.transform.scale(map_img, MAP_SIZE)
map_rect = map_img.get_rect()
map_rect = map_rect.move(MAP_POINT)

balloon1_img = pygame.image.load("balloon.png")
balloon1_img = pygame.transform.scale(balloon1_img, (ROAD_WIDTH, ROAD_WIDTH))
balloon1_img.set_alpha(120)

balloon2_img = pygame.image.load("balloon2.png")
balloon2_img = pygame.transform.scale(balloon2_img, (ROAD_WIDTH, ROAD_WIDTH))

upgrade_img = pygame.image.load("upward.png")
upgrade_img = pygame.transform.scale(upgrade_img, (ROAD_WIDTH, ROAD_WIDTH))
# upgrade_img.set_alpha()

play_img = pygame.image.load("play.png")
play_img = pygame.transform.scale(play_img, (ROAD_WIDTH, ROAD_WIDTH))

pause_img = pygame.image.load("pause.png")
pause_img = pygame.transform.scale(pause_img, (ROAD_WIDTH, ROAD_WIDTH))

tower1_img = pygame.image.load("tower.png")
tower1_img = pygame.transform.scale(tower1_img, (ROAD_WIDTH, ROAD_WIDTH))

tower2_img = pygame.image.load("tower2.png")
tower2_img = pygame.transform.scale(tower2_img, (ROAD_WIDTH, ROAD_WIDTH))

dart_img = pygame.image.load("needle.png")
dart_img = pygame.transform.flip(dart_img, True, False)
dart_img = pygame.transform.scale(dart_img, (40, 40))

star1_img = pygame.image.load("star.png")
star1_img = pygame.transform.scale(star1_img, (ROAD_WIDTH, ROAD_WIDTH))

star2_img = pygame.image.load("star2.png")
star2_img = pygame.transform.scale(star2_img, (ROAD_WIDTH, ROAD_WIDTH))


class Unit(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = []
        self.rect = None

    def move(self):
        self.rect = self.rect.move(self.speed)
        self.x, self.y = self.rect.center


class Dart_unit(Unit):
    def __init__(self, tower_p, target_p):
        super().__init__()
        self.x, self.y = tower_p
        self.speed = target_p[0] - self.x, target_p[1] - self.y
        self.speed = [i/np.linalg.norm(self.speed) * 5 for i in self.speed]
        self.rect = dart_img.get_rect()
        # self.rect = self.rect.fit(0, 0, 10, 10)
        self.rect.center = self.x, self.y

        # rotate dart img. i don't know why it works
        if self.speed[0] == 0:
            if self.speed[1]/abs(self.speed[1]) == 1:
                deg = 90
            else:
                deg = -90
        else:
            deg = 0 - np.rad2deg(np.arctan(self.speed[1]/self.speed[0]))
            if self.speed[0] < 0:
                deg += 180
        self.img = pygame.transform.rotate(dart_img, deg)
        self.dest = target_p


class Tower_unit(Unit):
    def __init__(self):
        super().__init__()
        self.attack_range = 100
        self.charge = False
        self.timer = None
        self.timer2 = None
        self.level = 1
        self.iden = None
        self.dest = None

    def attack(self):
        raise NotImplementedError

    def position(self):
        return self.x, self.y

    def set(self, position, iden):
        self.x, self.y = position
        self.rect = tower1_img.get_rect()
        self.rect.center = self.x, self.y
        self.timer = MyEvent(MAXFPS * 2)
        self.iden = iden

    def upgrade(self):
        self.level += 1
        if self.level == 2:
            self.timer2 = MyEvent(MAXFPS/5, False)
        return 5

    def find_target(self, ballooon):
        if np.sum((np.array([ballooon.x, ballooon.y]) - np.array([self.x, self.y]))**2) < self.attack_range**2:
            # print(np.sum((np.array([ballooon.x, ballooon.y]) - np.array([self.x, self.y]))**2) )
            # print(self.attack_range**2)
            # print("It can attack now")
            return True
        else:
            # print("It can not attack now")
            return False


class Balloon_unit(Unit):
    def __init__(self):
        super().__init__()
        self.reward = 0
        self.level = 0  # speed, life depends on balloon level

    def set(self, level):
        # self.rect = pygame.Rect(STARTING_POINT)
        self.rect = balloon1_img.get_rect()
        # self.rect = self.rect.fit(0, 0, 20, 20)  # the move
        # self.rect = self.rect.fit(ROAD_WIDTH - BALLOON_WIDTH, int(ROAD_WIDTH - BALLOON_WIDTH)/2, BALLOON_WIDTH, BALLOON_WIDTH)  # It is resized cented at left-upper point
        self.rect = self.rect.move(STARTING_POINT)
        self.x, self.y = self.rect.center
        # print("center is", self.rect.center)
        self.level = level
        self.speed = [1, 0]
        # print('balloon rect size is : ', self.rect)


class MyEvent(object):
    def __init__(self, interval, able=True):
        if interval < 1:
            print("minimum interval is 1")
            raise ValueError
        self.count = 0
        self.fin = int(interval)
        self.able = able

    def inc(self):
        if self.able:
            self.count += 1
            if (self.fin - self.count) > 0:
                return False
            else:
                self.count = 0
                return True
        else:
            return False


class Button(object):
    def __init__(self, img, position, iden):
        self.img = img
        self.pos = position
        self.butt_img_rect = None
        self.iden = iden

    def draw(self, screen):
        butt_img = pygame.Surface(ICON_SIZE)
        butt_img.fill(COLORS[ICON])
        butt_img.blit(self.img, (5, 5))
        screen.blit(butt_img, self.pos)
        self.butt_img_rect = butt_img.get_rect()
        self.butt_img_rect.x, self.butt_img_rect.y = self.pos[0], self.pos[1]



class TD_App(object):
    def __init__(self):
        # pygame setting
        pygame.init()
        self.default_font = pygame.font.Font(
            pygame.font.get_default_font(), 20
        )

        # screen setting
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.event.set_blocked((pygame.VIDEOEXPOSE, pygame.VIDEORESIZE))

        # status of the stage
        self.life = 10  # If life == 0 --> gameover
        self.score = 0
        self.point = 5
        self.sel_info = [None, -1]
        self.now_p = None

        # helper for balloon making
        self.balloon_data_row = None
        self.balloon_data_index = 0
        self.balloon_timer = MyEvent(1000, False)
        self.balloon_level = 0
        self.balloon_count = 0

        # status of overall game
        self.gameover = False
        self.paused = False
        self.stage = 1

        # mouse state
        self.ready2make_tower = False
        self.click_point = None

    def draw_unit(self, unit, name):
        p = unit.rect.x, unit.rect.y
        # eval("self.screen.blit(" + name + "_img, p")
        if name == "dart":
            self.screen.blit(unit.img, p)
        elif name == "tower1":
            self.screen.blit(tower1_img, p)
        elif name == "tower2":
            self.screen.blit(tower2_img, p)
        elif name == "balloon1":
            self.screen.blit(balloon1_img, p)
        elif name == "balloon2":
            self.screen.blit(balloon2_img, p)
        elif name == "star1":
            self.screen.blit(star1_img, p)
        elif name == "star2":
            self.screen.blit(star2_img, p)

    def disp_msg(self, msg, topleft):
        x, y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    COLORS[MSG]),
                (x, y))
            y += 24

    def make_button(self, position, button_img=False):
        new_img = pygame.Surface(ICON_SIZE)
        new_img.fill(COLORS[ICON])
        new_img.blit(button_img, (5, 5))
        self.screen.blit(new_img, position)
        new_img_rect = new_img.get_rect()
        new_img_rect.center=(position[0] +ICON_SIZE[0]/2, position[1] + ICON_SIZE[1]/2)
        return new_img_rect

    def ghost_tower(self, position1, tower_img):
        new_img = pygame.Surface(ICON_SIZE)
        # new_img = pygame.Surface.convert_alpha(tower_img)
        new_img.set_alpha(50)
        new_img.blit(tower_img, (5,5))
        img_center = position1[0] - ICON_SIZE[0] / 2, position1[1] - ICON_SIZE[1] / 2
        self.screen.blit(new_img, img_center)

    def icon_select(self, point):
        for temp_button in BUTTON:
            icon_rect = temp_button.butt_img_rect
            iden = temp_button.iden
            click_icon = False
            if icon_rect.collidepoint(point):
                print('Clicking Icon')
                click_icon = True
                print('identity : ', iden)
                break
            else:
                print('Not Clicking Icon')

        if click_icon == True:
            if iden == 0 :
                return [click_icon, iden]
            elif iden == 1:
                return [click_icon, iden]
            elif iden == 2:
                self.upgrade()
                return [False, None]
            elif iden == 3:
                self.toggle_pause()
                return [False, None]
        else:
            print('Wrong id')
            return [click_icon, None]

    def run(self):
        key_actions = {
            'ESCAPE': sys.exit,
            'p': self.toggle_pause
        }

        self.start_stage()
        fps_clk = pygame.time.Clock()

        button1 = Button(tower1_img, (820, 30), 0)
        button2 = Button(star1_img, (820, 100), 1)
        button3 = Button(upgrade_img, (820, 300), 2)
        button4 = Button(pause_img, (820, 500), 3)
        BUTTON.append(button1)
        BUTTON.append(button2)
        BUTTON.append(button3)
        BUTTON.append(button4)

        while True:
            fps_clk.tick(MAXFPS)
            if self.paused == True:
                self.screen.fill((255, 255, 255))
                self.disp_msg('Game Paused', (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        for key in key_actions:
                            if event.key == eval("pygame.K_" + key):
                                key_actions[key]()
            else:
                # draw screen
                self.screen.fill((255, 255, 255))
                self.screen.blit(map_img, map_rect.topleft)

                # draw objects
                current_node = TOWERS.head_node.tail
                while current_node != TOWERS.tail_node:
                    cur_twr = current_node.value
                    if cur_twr.iden == 0:
                        self.draw_unit(cur_twr, "tower" + str(cur_twr.level))
                    elif cur_twr.iden == 1:
                        self.draw_unit(cur_twr, "star" + str(cur_twr.level))
                    current_node = current_node.tail

                current_node = BALLOONS.head_node.tail
                while current_node != BALLOONS.tail_node:
                    cur_bln = current_node.value
                    self.draw_unit(cur_bln, "balloon" + str(cur_bln.level))
                    current_node = current_node.tail

                current_node = DARTS.head_node.tail
                while current_node != DARTS.tail_node:
                    self.draw_unit(current_node.value, "dart")
                    current_node = current_node.tail

                pygame.draw.rect(self.screen, COLORS[INTERFACE],
                                 pygame.Rect(0, 0, map_rect.right, map_rect.top))
                pygame.draw.rect(self.screen, COLORS[INTERFACE],
                                 pygame.Rect(map_rect.right, 0, SCREEN_SIZE[0] - map_rect.right, SCREEN_SIZE[1]))

                if self.ready2make_tower:
                    cursor_position = pygame.mouse.get_pos()
                    if self.now_p == 0:
                        self.ghost_tower(cursor_position, tower1_img)
                    else:
                        self.ghost_tower(cursor_position, star1_img)

                # display tower buttons
                button1.draw(self.screen)
                button2.draw(self.screen)
                button3.draw(self.screen)
                button4.draw(self.screen)

                # display status
                self.disp_msg("Stage : " + str(self.stage), (20, 40))
                self.disp_msg("Score : " + str(self.score), (150, 40))
                self.disp_msg("Life : " + str(self.life), (280, 40))
                self.disp_msg("Point : "+ str(self.point), (410, 40))

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if pygame.mouse.get_pressed()[0]:  # when left click
                        click_spot = pygame.mouse.get_pos()
                        click_used = False
                        temp_self_info = self.icon_select(click_spot)
                        self.now_p = temp_self_info[1]
                        # print('click spot is ', click_spot)
                        if self.ready2make_tower == False and 4 < self.point and self.sel_info[1] is not None:
                            self.sel_info = temp_self_info
                            self.ready2make_tower = self.sel_info[0]
                            click_used = True

                        if self.ready2make_tower == True and click_used == False and self.sel_info[1] is not None:
                            if self.create_tower(click_spot, self.sel_info[1]):
                                self.ready2make_tower = False
                                self.point -= 5
                        else:
                            print('You cannot build tower')
                    elif event.type == pygame.KEYDOWN:
                        for key in key_actions:
                            if event.key == eval("pygame.K_" + key):
                                key_actions[key]()

                # handle balloon timer
                if self.balloon_timer.inc():
                    self.create_balloon(self.balloon_level)
                    if self.balloon_count == 0:
                        self.balloon_data_index += 3
                        try:
                            if self.balloon_data_row[self.balloon_data_index].value:
                                self.balloon_level = self.balloon_data_row[self.balloon_data_index].value
                                self.balloon_count = self.balloon_data_row[self.balloon_data_index + 1].value
                                self.balloon_timer.fin = MAXFPS * self.balloon_data_row[self.balloon_data_index + 2].value
                            else:
                                self.balloon_timer.able = False
                        except IndexError:
                            self.balloon_timer.able = False

                # handle towers
                current_node = TOWERS.head_node.tail
                while current_node != TOWERS.tail_node:
                    # handle tower timer
                    twr = current_node.value
                    if twr.timer.inc():
                        twr.charge = True  # tower charging is ok
                        twr.timer.able = False  # suspend timer
                    if twr.timer2 is not None:
                        if twr.timer2.inc():
                            twr.timer.able = True
                            twr.timer2.able = False
                            self.create_dart(twr.position(), twr.dest)
                    # do tower action
                    if twr.charge:
                        temp_node = BALLOONS.head_node.tail
                        while temp_node != BALLOONS.tail_node:
                            if twr.find_target(temp_node.value):
                                self.tower_attack(twr, temp_node.value)
                                twr.timer.able = True
                                twr.charge = False
                                break
                            temp_node = temp_node.tail

                    current_node = current_node.tail

                # handle darts
                temp_node = DARTS.head_node.tail
                while temp_node != DARTS.tail_node:
                    temp_dart = temp_node.value
                    if not self.out_of_map(temp_dart):
                        temp_dart.move()
                        lst = BALLOONS.to_list()
                        collide_detector = temp_dart.rect.collidelist(lst[0])
                        if not collide_detector == -1:
                            DARTS.delete(temp_node)
                            lst[0][collide_detector].level -= 1
                            if lst[0][collide_detector].level == 0:
                                BALLOONS.delete(lst[1][collide_detector])
                            self.score += 1
                            self.point += 1
                        else:
                            if self.out_of_range((temp_dart.x, temp_dart.y), temp_dart.dest):
                                DARTS.delete(temp_node)
                    else:
                        DARTS.delete(temp_node)
                    temp_node = temp_node.tail

                # do balloon action
                current_node = BALLOONS.head_node.tail
                while current_node != BALLOONS.tail_node:
                    bln = current_node.value
                    bln.move()
                    # change speed at turning point
                    if bln.rect.center == (STARTING_POINT_CENTER[0] + 470, STARTING_POINT_CENTER[1]):
                        bln.speed = [0, -1]
                    elif bln.rect.center == (STARTING_POINT_CENTER[0] + 470, STARTING_POINT_CENTER[1] - 310):
                        bln.speed = [1, 0]
                    elif self.out_of_map(bln):
                        self.life -= bln.level
                        BALLOONS.delete(current_node)
                    current_node = current_node.tail

                if BALLOONS.head_node.tail == BALLOONS.tail_node and (not self.balloon_timer.able):
                    if self.stage < 5:
                        self.stage += 1
                        self.start_stage()

                if self.life < 1:
                    self.gameover = True
                    break

        if self.gameover:
            self.screen.fill((0, 0, 0))
            self.screen.blit(
                pygame.font.Font(pygame.font.get_default_font(), 50).render(
                    "Game over!",
                    True,
                    (255, 255, 255)
                ),
                (100, 330)
            )
            pygame.display.update()
            pygame.event.clear()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        return

    # toggle self.paused variable
    def toggle_pause(self):
        self.paused = not self.paused

    def create_dart(self, start_p, dest_p):
        new_unit = Dart_unit(start_p, dest_p)
        DARTS.insert_value(new_unit)

    # create balloon
    def create_balloon(self, level):
        temp = Balloon_unit()
        temp.set(level)
        BALLOONS.insert_value(temp)
        self.balloon_count -= 1

    def create_tower(self, position, iden):
        temp = Tower_unit()
        temp.set(position, iden)
        if temp.rect.collidelist(TOWERS.to_list()[0]) == -1 and self.out_of_map(temp) is False:
            TOWERS.insert_value(temp)
            return True
        else:
            print('not working')

    def tower_attack(self, tower, balloon):
        if tower.iden == 0:
            if tower.level == 1:
                self.create_dart(tower.position(), (balloon.x, balloon.y))
            elif tower.level == 2:
                self.create_dart(tower.position(), (balloon.x, balloon.y))
                tower.dest = balloon.x, balloon.y
                tower.timer.able = False
                tower.timer2.able = True
            else:
                raise NotImplementedError
        elif tower.iden == 1:
            deg = 2 * np.pi / 5
            self.create_dart(tower.position(), (tower.x, tower.y - tower.attack_range))
            self.create_dart(tower.position(), (
                tower.x - int(tower.attack_range * np.sin(deg)),
                tower.y - int(tower.attack_range * np.cos(deg))))
            self.create_dart(tower.position(), (
                tower.x - int(tower.attack_range * np.sin(2 * deg)),
                tower.y - int(tower.attack_range * np.cos(2 * deg))))
            self.create_dart(tower.position(), (
                tower.x - int(tower.attack_range * np.sin(3 * deg)),
                tower.y - int(tower.attack_range * np.cos(3 * deg))))
            self.create_dart(tower.position(), (
                tower.x - int(tower.attack_range * np.sin(4 * deg)),
                tower.y - int(tower.attack_range * np.cos(4 * deg))))
        else:
            raise NotImplementedError

    def out_of_range(self, tower_p, dart_p):
        return np.sum(np.square(np.subtract(np.array(tower_p), np.array(dart_p)))) > 100 ** 2

    # initialize variable and timer to start each stage
    def start_stage(self):
        self.balloon_data_row = ws[self.stage + 1]
        self.balloon_data_index = 1
        self.balloon_level = self.balloon_data_row[self.balloon_data_index].value
        self.balloon_count = self.balloon_data_row[self.balloon_data_index + 1].value
        self.balloon_timer.count = 0
        self.balloon_timer.fin = MAXFPS * self.balloon_data_row[self.balloon_data_index + 2].value
        self.balloon_timer.able = True
        self.ready2make_tower = False
        self.click_point = None

    def out_of_map(self, unit):
        X = map_rect.collidepoint(unit.rect.topleft)
        X = X or map_rect.collidepoint(unit.rect.topright)
        X = X or map_rect.collidepoint(unit.rect.bottomleft)
        X = X or map_rect.collidepoint(unit.rect.bottomright)
        if X:
            return False
        return True

    # function to test or debug
    def test(self):
        pass  # not to be compile error


if __name__ == '__main__':
    TD = TD_App()
    TD.run()