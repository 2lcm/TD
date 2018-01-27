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
MK_TOWER, MK_STAR, UPGRADE, PP = 0, 1, 2

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

play_img = pygame.image.load("play.png")
play_img = pygame.transform.scale(play_img, (ROAD_WIDTH, ROAD_WIDTH))

pause_img = pygame.image.load("pause.png")
pause_img = pygame.transform.scale(pause_img, (ROAD_WIDTH, ROAD_WIDTH))

tower_img = pygame.image.load("tower.png")
tower_img = pygame.transform.scale(tower_img, (ROAD_WIDTH, ROAD_WIDTH))

tower2_img = pygame.image.load("tower2.png")
tower2_img = pygame.transform.scale(tower2_img, (ROAD_WIDTH, ROAD_WIDTH))

dart_img = pygame.image.load("needle.png")
dart_img = pygame.transform.flip(dart_img, True, False)
dart_img = pygame.transform.scale(dart_img, (40, 40))


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
    def __init__(self, tower, target):
        super().__init__()
        self.x, self.y = tower.x, tower.y
        self.speed = target.x - self.x, target.y - self.y
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


class Tower_unit(Unit):
    def __init__(self):
        super().__init__()
        self.attack_range = 100
        self.charge = False
        self.timer = None

    def attack(self):
        raise NotImplementedError

    def position(self):
        return self.x, self.y

    def set(self, position):
        self.x, self.y = position
        self.rect = tower_img.get_rect()
        self.rect.center = self.x, self.y
        self.timer = MyEvent(MAXFPS)

    def upgrade(self):
        pass

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
        print("center is", self.rect.center)
        self.level = level
        self.speed = [1, 0]
        print('balloon rect size is : ', self.rect)


class MyEvent(object):
    def __init__(self, interval, able=True):
        if (interval <=0) or (type(interval) != int):
            print("interval must be positive integer")
            sys.exit()
        self.count = 0
        self.fin = interval
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
    def __init__(self, img, position):
        self.img = img
        self.pos = position

    def draw(self):
        butt_img = pygame.Surface(ICON_SIZE)
        butt_img.fill(COLORS[ICON])
        butt_img.blit(self.img, (5, 5))
        butt_img_rect = butt_img.get_rect(butt_img)
        butt_img_rect.center = self.pos[0] - ICON_SIZE[0], self.pos[1] - ICON_SIZE[1]

    def oper(self, id, click_spot):
        self.id = id
        self.click = click_spot
        if id == 0:
            TD_App.create_tower(self.id, self.click)
        elif id == 1:
            TD_App.create_tower(self.id, self.click)
        elif id == 2:
            OBJECT.upgrade()
        elif id == 3:
            TD_App.toggle_pause()

        else:
            print('Wrong id')

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
        elif name == "tower":
            self.screen.blit(tower_img, p)
        elif name == "balloon1":
            self.screen.blit(balloon1_img, p)
        elif name == "balloon2":
            self.screen.blit(balloon2_img, p)

    def draw_unit_test(self, unit, ty):
        p = unit.rect.x, unit.rect.y
        print(p)
        eval("self.screen.blit(" + ty + "_img, p)")

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

    def ghost_tower(self, position1):
        new_img = pygame.Surface(ICON_SIZE)
        new_img.set_alpha(50)
        new_img.blit(tower_img, (5,5))
        img_center = position1[0] - ICON_SIZE[0] / 2, position1[1] - ICON_SIZE[1] / 2
        # print(position1)
        print(img_center)
        self.screen.blit(new_img, img_center)

    def icon_select(self, icon_rect, point):
        if icon_rect.collidepoint(point):
            print('Clicking Icon')
            return True
        else:
            print('Not Clicking Icon')
            return False

    def run(self):
        key_actions = {
            'ESCAPE': sys.exit,
            'p': self.toggle_pause
        }

        self.start_stage()
        fps_clk = pygame.time.Clock()

        while True:
            fps_clk.tick(MAXFPS)
            if self.paused == True:
                self.screen.fill((255,255,255))
                self.disp_msg('Game Paused', (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2))
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
                    self.draw_unit(current_node.value, "tower")
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
                if self.ready2make_tower == True:
                    cursor_position = pygame.mouse.get_pos()
                    self.ghost_tower(cursor_position)

                # display tower buttons
                button1 = self.make_button((820, 30), tower_img)
                # display status
                self.disp_msg("Stage : " + str(self.stage), (20, 40))
                self.disp_msg("Score : " + str(self.score), (150, 40))
                self.disp_msg("Life : " + str(self.life), (280, 40))
                self.disp_msg("Point : "+ str(self.point), (410, 40))

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if pygame.mouse.get_pressed()[0]: # when left click
                        click_spot = pygame.mouse.get_pos()
                        click_used = False
                        # print('click spot is ', click_spot)
                        if self.ready2make_tower == False and 4 < self.point:
                            self.ready2make_tower = self.icon_select(button1, click_spot)
                            click_used = True

                        if self.ready2make_tower == True  and click_used == False:
                            if self.create_tower(click_spot):
                                self.ready2make_tower = False
                                self.point -=5
                        else:
                            print('Not enough point to build tower')
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
                    if current_node.value.timer.inc():
                        current_node.value.charge = True  # tower charging is ok
                        current_node.value.timer.able = False  # suspend timer
                    # do tower action
                    if current_node.value.charge:
                        temp_node = BALLOONS.head_node.tail
                        while temp_node != BALLOONS.tail_node:
                            if current_node.value.find_target(temp_node.value):
                                self.create_dart(current_node.value, temp_node.value)
                                current_node.value.timer.able = True
                                current_node.value.charge = False
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

    def create_dart(self, tower, target):
        # new_node = LinkedList.NODE(Dart_unit(tower_index, target_index))
        # DARTS.insert(new_node)
        new_unit = Dart_unit(tower, target)
        DARTS.insert_value(new_unit)

    # create balloon
    def create_balloon(self, level):
        temp = Balloon_unit()
        temp.set(level)
        BALLOONS.insert_value(temp)
        self.balloon_count -= 1

    def create_tower(self, position):
        temp = Tower_unit()
        temp.set(position)

        if temp.rect.collidelist(TOWERS.to_list()[0]) == -1 and self.out_of_map(temp) is False:
            TOWERS.insert_value(Tower_unit())
            TOWERS.tail_node.head.value.set(position)

            return True
        else:
            print('not working')

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

# comments not to usage
# test
#########################
## It is just for testing
# test_tower = Tower_unit()
# test_tower.attack()
#########################
#########################
## It is just for testing
# temp_balloon = Balloon_unit()
# temp_balloon.move()
############################################
# def balloon_storage(self):
#     for i in range(5):
#         temp_balloon = Balloon_unit()
#         temp_balloon.set(1)
#         BALLOONS.append(temp_balloon)
#############################################
