import pygame
import sys
import numpy as np
<<<<<<< HEAD
import LinkedList

=======
>>>>>>> bc67d6c7eda40c27aaf47a234ebee1d8bf89ef50

# constants
SCREEN_SIZE = 1000, 700
MAP_SIZE = 800, 600
ROAD_WIDTH = 55
BALLOON_WIDETH = 20
MAP_POINT = 0, 100
STARTING_POINT = -ROAD_WIDTH, 545 - BALLOON_WIDETH
STARTING_POINT_CENTER = STARTING_POINT[0] + int(ROAD_WIDTH/2), STARTING_POINT[1] + int(ROAD_WIDTH/2)
ICON_SIZE = (65, 65)
MAXFPS = 50

# colors,,kki
INTERFACE, MSG, ICON = 0, 1, 2

COLORS = [
    (int(0xCC), int(0xCC), int(0xCC)),
    (0, 0, 0),
    (int(0x55), int(0x55), int(0x55))
]

# data structures (list) to control units
TOWERS = []
# TOWERS = LinkedList.LL()
BALLOONS = []
DARTS = []
# DARTS = LinkedList.LL()
TIMERS = []
# Index | meaning(?)
# 0 :
database = []

map_img = pygame.image.load("map1.png")
map_img = pygame.transform.scale(map_img, MAP_SIZE)
map_rect = map_img.get_rect()
map_rect = map_rect.move(MAP_POINT)

balloon_img = pygame.image.load("balloon.png")
balloon_img = pygame.transform.scale(balloon_img, (ROAD_WIDTH, ROAD_WIDTH))

tower_img = pygame.image.load("tower.png")
tower_img = pygame.transform.scale(tower_img, (ROAD_WIDTH, ROAD_WIDTH))

dart_img = pygame.image.load("needle.png")
dart_img = pygame.transform.flip(dart_img, True, False)
dart_img = pygame.transform.scale(dart_img, (40, 40))

<<<<<<< HEAD


=======
# will change to linked list
TOWERS = []
BALLOONS = []
DARTS = []
>>>>>>> bc67d6c7eda40c27aaf47a234ebee1d8bf89ef50


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
    def __init__(self, tower_index, target_index):
        super().__init__()
        self.x, self.y = TOWERS[tower_index].x, TOWERS[tower_index].y
        self.speed = BALLOONS[target_index].x - self.x, BALLOONS[target_index].y - self.y
        self.speed = [i/np.linalg.norm(self.speed) * 5 for i in self.speed]
        self.rect = dart_img.get_rect()
        self.rect = self.rect.fit(0,0,10,10)
        self.rect.center = self.x, self.y
        # self.dest = TOWERS[tower_index]  # final destination
        # rotate dart img. i dont know why it works
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
        #self.expense = 0
        self.charge = False
        self.myballoon_index = None
        self.timer = None

    def attack(self):
        raise NotImplementedError

    def position(self):
        return (self.x, self.y)

    def set(self, position):
        self.x, self.y = position
        self.rect = tower_img.get_rect()
        self.rect.center = self.x, self.y
        self.timer = MyEvent(MAXFPS)

    def upgrade(self):
        pass

    def find_target(self, myballoon):
        if np.sum((np.array([myballoon.x, myballoon.y]) - np.array([self.x, self.y]))**2) < self.attack_range**2:
            # print(np.sum((np.array([myballoon.x, myballoon.y]) - np.array([self.x, self.y]))**2) )
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
        self.rect = balloon_img.get_rect()
        # self.rect = self.rect.fit(0, 0, 20, 20)  # the move
        self.rect = self.rect.fit(ROAD_WIDTH -BALLOON_WIDETH, int(ROAD_WIDTH-BALLOON_WIDETH)/2,BALLOON_WIDETH,BALLOON_WIDETH) # It is resized cented at left-upper point
        self.rect = self.rect.move(STARTING_POINT)
        self.x, self.y = self.rect.center
        print("center is", self.rect.center)
        self.level = level
        self.speed = [1, 0]
        print('balloon rect size is : ', self.rect)


class MyEvent(object):
    def __init__(self, interval, able = True):
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
        self.budget = 0  # money to install unit
        self.life = 0  # If life == 0 --> gameover
        self.score = 0
        self.balloon_timer = None

        # status of overall game
        self.gameover = False
        self.paused = False
        self.stage = 1

    def draw_unit(self, unit, ty):
        p = unit.rect.x, unit.rect.y
        if ty == "dart":
            self.screen.blit(unit.img, p)
        else:
            eval("self.screen.blit(" + ty + "_img, p)")

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

    def make_button(self, img):
        new_img = pygame.Surface(ICON_SIZE)
        pygame.draw.rect(new_img, COLORS[ICON],
                         pygame.Rect((0, 0), ICON_SIZE))
        new_img.blit(img, (5, 5))
        return new_img

    def run(self):
        key_actions = {
            'ESCAPE': sys.exit,
            'p': self.toggle_pause
        }

        self.start_stage()
        fps_clk = pygame.time.Clock()

        while True:
            # draw screen
            self.screen.fill((255, 255, 255))
            self.screen.blit(map_img, map_rect.topleft)
            for i in range(len(TOWERS)):
                self.draw_unit(TOWERS[i], "tower")
            for i in range(len(BALLOONS)):
                self.draw_unit(BALLOONS[i], "balloon")
            for i in range(len(DARTS)):
                self.draw_unit(DARTS[i], "dart")
            # while True:
            #     current_Node = DARTS.head_node.tail
            #     if current_Node == DARTS.tail_node:
            #         break
            #     self.draw_unit(current_Node.value, "balloon")
            #     current_Node = current_Node.tail

            pygame.draw.rect(self.screen, COLORS[INTERFACE],
                             pygame.Rect(0, 0, map_rect.right, map_rect.top))
            pygame.draw.rect(self.screen, COLORS[INTERFACE],
                             pygame.Rect(map_rect.right, 0, SCREEN_SIZE[0] - map_rect.right, SCREEN_SIZE[1]))
            # display tower buttons
            button_img = self.make_button(tower_img)
            self.screen.blit(button_img, (820, 30))
            # display status
            self.disp_msg("Stage : " + str(self.stage), (20, 40))
            self.disp_msg("Score : " + str(self.score), (150, 40))
            self.disp_msg("Life : " + str(self.life), (280, 40))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif pygame.mouse.get_pressed()[0]: # when left click
                    click_spot = pygame.mouse.get_pos()
                    # print('click spot is ', click_spot)
                    self.create_tower(click_spot)

                    # print(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_" + key):
                            key_actions[key]()

            # handle balloon timer
            if self.balloon_timer.inc():
                self.create_balloon()

            # handle towers
            for tower_index in range(len(TOWERS)):
                temp_tower = TOWERS[tower_index]
                # handle tower timer
                if temp_tower.timer.inc():
                    temp_tower.charge = True  # tower charging is ok
                    temp_tower.timer.able = False  # suspend timer
                # do tower action
                if temp_tower.charge:
                    for temp_index in range(len(BALLOONS)):
                        if temp_tower.find_target(BALLOONS[temp_index]):
                            self.create_dart(tower_index, temp_index)
                            temp_tower.timer.able = True
                            temp_tower.charge = False
                            break
                            
            # do dart action
            for dart_index in range(len(DARTS)-1, -1, -1):
                temp_dart = DARTS[dart_index]
                if not self.out_of_map(temp_dart):
                    temp_dart.move()
                    collide_detector = temp_dart.rect.collidelist(BALLOONS)
                    if not collide_detector == -1:
                        DARTS.remove(temp_dart)
                        BALLOONS.remove(BALLOONS[collide_detector])
                        self.score +=1
                else:
                    DARTS.remove(temp_dart)
            # while True:
            #     temp_node = DARTS.head_node.tail
            #     if temp_node == DARTS.tail_node:
            #         break
            #     temp_dart = temp_node.value
            #     if not self.out_of_map(temp_dart):
            #         temp_dart.move()
            #         collide_detector = temp_dart.rect.collidelist(BALLOONS)
            #         if not collide_detector == -1:
            #             DARTS.delete(temp_node)
            #             BALLOONS.remove(BALLOONS[collide_detector])
            #             self.score +=1
            #     else:
            #         DARTS.delete(temp_node)

            # do balloon action
            for balloon_index in range(len(BALLOONS)-1, -1, -1):
                bln = BALLOONS[balloon_index]
                bln.move()
                # change speed at turning point
                if bln.rect.center == (STARTING_POINT_CENTER[0] + 470 - BALLOON_WIDETH, STARTING_POINT_CENTER[1]):
                    bln.speed = [0, -1]
                elif bln.rect.center == (STARTING_POINT_CENTER[0] + 470 - BALLOON_WIDETH, STARTING_POINT_CENTER[1] - 310):
                    bln.speed = [1, 0]
                elif self.out_of_map(bln):
                    del BALLOONS[balloon_index]
                    self.life -= 1
            if self.life < 1:
                self.gameover = True
                break
                
            # do dart action
            
            fps_clk.tick(MAXFPS)

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

    def create_dart(self, tower_index, target_index):
        # new_node = LinkedList.NODE(Dart_unit(tower_index, target_index))
        # DARTS.insert(new_node)
        new_unit = Dart_unit(tower_index, target_index)
        DARTS.append(new_unit)

    # create balloon
    def create_balloon(self):
        BALLOONS.append(Balloon_unit())
        BALLOONS[-1].set(1)

    def create_tower(self, position):
        temp = Tower_unit()
        temp.set(position)
        print(temp.rect.collidelist(TOWERS[:-1]))
        if temp.rect.collidelist(TOWERS) == -1:
            TOWERS.append(Tower_unit())
            TOWERS[-1].set(position)
<<<<<<< HEAD
            TIMERS.append(MyEvent(MAXFPS))
=======
>>>>>>> bc67d6c7eda40c27aaf47a234ebee1d8bf89ef50
        else:
            print('not working')

    # initialize variable and timer to start each stage
    def start_stage(self):
        self.budget = 0
        self.life = 1
<<<<<<< HEAD
        TIMERS.append(MyEvent(MAXFPS * 2))
=======
        self.balloon_timer = MyEvent(MAXFPS * 2)
>>>>>>> bc67d6c7eda40c27aaf47a234ebee1d8bf89ef50

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
        self.start_stage()

        self.create_balloon()

        while True:
            # draw screen
            self.screen.fill((255, 255, 255))
            self.screen.blit(map_img, (0, 0))
            for i in range(len(BALLOONS)):
                self.draw_unit(BALLOONS[i], "balloon")

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
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
