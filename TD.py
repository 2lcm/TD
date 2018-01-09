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
dart_img = pygame.transform.scale(dart_img, (10,10))


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
        self.rect = dart_img.get_rect()
        self.rect.center = self.x, self.y


class Tower_unit(Unit):
    def __init__(self):
        super().__init__()
        self.attack_range = 0
        #self.expense = 0
        self.action = False

    def position(self):
        return (self.x, self.y)

    def set(self, position):
        self.x, self.y = position
        self.attack_range = 500
        self.rect = tower_img.get_rect()
        self.rect.center = self.x, self.y

    def upgrade(self):
        pass

    def find_target(self, balloon_x, balloon_y):
        temp_balloon = np.array([balloon_x, balloon_y])

        if np.sum((temp_balloon - np.array([self.x, self.y]))**2) < self.attack_range**2:
            print("It can attack now")
            return True
        else:
            print("It can not attack now")
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
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_" + key):
                            key_actions[key]()
                else:
                    if event.type == pygame.USEREVENT + 1:  # generating balloon timer
                        self.create_balloon()
                    for i in range(len(TOWERS)):
                        if event.type == pygame.USEREVENT + i + 2:
                            TOWERS[i].action = True

            # do tower action
            for tower_index in range(len(TOWERS)):
                pass

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

    # create balloon
    def create_balloon(self):
        BALLOONS.append(Balloon_unit())
        BALLOONS[-1].set(1)

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
#########################
