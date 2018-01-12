import pygame
import sys
import numpy as np
import time

maxfps = 100

# pygame.USEREVENT list
# USEREVENT + 1 : balloon generating timer
# USEREVENT + 2 + i : attacking timer of towers[i]

# constants
SCREEN_SIZE = 1000, 700
MAP_SIZE = 800, 600
ROAD_WIDTH = 55
MAP_POINT = 0, 100
STARTING_POINT = -ROAD_WIDTH, 545
STARTING_POINT_CENTER = STARTING_POINT[0] + int(ROAD_WIDTH/2), STARTING_POINT[1] + int(ROAD_WIDTH/2)

TOWERS = []
BALLOONS = []
DARTS = []

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
dart_img = pygame.transform.scale(dart_img, (100,100))


TOWERS = []
BALLOONS = []
DARTS = []


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
        self.rect.center = self.x, self.y


class Tower_unit(Unit):
    def __init__(self):
        super().__init__()
        self.attack_range = 100
        #self.expense = 0
        self.action = False
        self.myballoon_index = None

    def attack(self):
        if self.action == True:
            Dart_unit


    def position(self):
        return (self.x, self.y)

    def set(self, position):
        self.x, self.y = position
        self.rect = tower_img.get_rect()
        self.rect.center = self.x, self.y

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
        self.rect = self.rect.move(STARTING_POINT)
        self.x, self.y = self.rect.center
        self.level = level
        self.speed = [1, 0]


class TD_App(object):
    def __init__(self):
        # pygame setting
        pygame.init()
        # self.default_font = pygame.font.Font(
        #     pygame.font.get_default_font(), 12
        # )

        # screen setting
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        # status of the stage
        self.budget = 0  # money to install unit
        self.life = 0  # If life == 0 --> gameover

        # status of overall game
        self.gameover = False
        self.paused = False
        self.stage = 1

    def draw_unit(self, unit, ty):
        p = unit.rect.x, unit.rect.y
        eval("self.screen.blit(" + ty + "_img, p)")


    def run(self):
        key_actions = {
            'ESCAPE': sys.exit,
            'p': self.toggle_pause
        }


        self.start_stage()

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

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif pygame.mouse.get_pressed()[0]: # when left click
                    click_spot = pygame.mouse.get_pos()
                    self.create_tower(click_spot)

                    # print(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_" + key):
                            key_actions[key]()
                else:
                    if event.type == pygame.USEREVENT + 1:  # generating balloon timer
                        self.create_balloon()
                    for i in range(len(TOWERS)):
                        if event.type == pygame.USEREVENT + i + 2 :
                            TOWERS[i].action = True
                            pygame.time.set_timer(pygame.USEREVENT + i + 2, 0)
                        else:
                            pass
                            # DARTS



            # do tower action
            for tower_index in range(len(TOWERS)):
                temp_tower = TOWERS[tower_index]
                if temp_tower.action:
                    for temp_index in range(len(BALLOONS)):
                        if temp_tower.find_target(BALLOONS[temp_index]):
                            print("create dart is working here")
                            self.create_dart(tower_index, temp_index)
                            pygame.time.set_timer(pygame.USEREVENT + tower_index + 2, 1000)
                            temp_tower.action = False
                            break
            # for tower_index in range(len(TOWERS)):
            #     temp_tower = TOWERS[tower_index]
            #     if temp_tower.action:
            #         if temp_tower.myballoon_index != None and temp_tower.find_target(BALLOONS[temp_tower.myballoon_index]) == True:
            #             # pygame.time.set_timer(pygame.USEREVENT + tower_index + 2, 1000)
            #             target_index = temp_tower.myballoon_index
            #             # print('my balloon position : ', BALLOONS[target_index].x)
            #             print('Tower{} is attacking balloon {}'.format(tower_index, target_index))
            #             self.create_dart(tower_index, target_index)
            #             temp_tower.action = False
            #         else:
            #             temp_tower.myballoon_index = None
            #         if temp_tower.myballoon_index == None:
            #             for temp_index in range(len(BALLOONS)):
            #                 if temp_tower.find_target(BALLOONS[temp_index]):
            #                     temp_tower.myballoon_index = temp_index
            #                     self.create_dart(tower_index, target_index)
            #                     temp_tower.action = False
            #                     break


            for dart_index in range(len(DARTS)-1, -1, -1):
                temp_dart = DARTS[dart_index]
                if not self.out_of_map(temp_dart):
                    temp_dart.move()
                else:
                    DARTS.remove(temp_dart)



            # do balloon action
            for balloon_index in range(len(BALLOONS)-1, -1, -1):
                bln = BALLOONS[balloon_index]
                bln.move()
                # change speed at turning point
                if bln.rect.center == (STARTING_POINT_CENTER[0] + 470, STARTING_POINT_CENTER[1]):
                    bln.speed = [0, -1]
                elif bln.rect.center == (STARTING_POINT_CENTER[0] + 470, STARTING_POINT_CENTER[1] - 310):
                    bln.speed = [1, 0]
                elif self.out_of_map(bln):
                    del BALLOONS[balloon_index]


    # toggle self.paused variable
    def toggle_pause(self):
        self.paused = not self.paused
    def create_dart(self, tower_index, target_index):
        DARTS.append(Dart_unit(tower_index, target_index))


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
            pygame.time.set_timer(pygame.USEREVENT + len(TOWERS) + 1, 1000)
        else:
            print('not working')


    # initialize variable and timer to start each stage
    def start_stage(self):
        self.budget = 0
        self.life = 10
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

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
