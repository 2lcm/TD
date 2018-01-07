import pygame
import sys
import numpy as np
import time

# pygame.USEREVENT list
# USEREVENT + 1 : balloon generating timer
# USEREVENT + 2 + i : attacking timer of towers[i]

# constants
SCREEN_SIZE = 1000, 700
ROAD_WIDTH = 70
STARTING_POINT = 0, 500

TOWERS = []
BALLOONS = []
DARTS = []

# Index | meaning(?)
# 0 :
database = []

map_img = pygame.image.load("map1.png")
map_rect = map_img.get_rect()

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
        self.rect.center = self.x + self.speed[0], self.y + self.speed[1]


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
        #self.reward
        self.level = 0  # speed, life depends on balloon level

    def set(self, level):
        self.x, self.y = STARTING_POINT
        self.rect = balloon_img.get_rect()
        self.rect.center = self.x, self.y
        self.level = level
        self.speed = [1,0]


class TD_App(object):
    def __init__(self):
        # pygame setting
        pygame.init()
        # self.default_font = pygame.font.Font(
        #     pygame.font.get_default_font(), 12
        # )

        # screen setting
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        # money to install unit
        self.budget = 0
        # If life == 0 --> gameover
        self.life = 0

        # define self variable
        self.gameover = False
        self.paused = False

    def draw_unit(self, unit, tp):
        p = unit.rect.x, unit.rect.y
        eval("self.screen.blit(" + tp + "_img, p)")

    def balloon_storage(self):
        for i in range(5):
            temp_balloon = Balloon_unit()
            temp_balloon.set(1)
            BALLOONS.append(temp_balloon)

    def run(self):
        key_actions = {
            'ESCAPE': sys.exit,
            'p': self.toggle_pause
        }

<<<<<<< HEAD
        pygame.time.set_timer(pygame.USEREVENT + 1 , 1000)

=======
>>>>>>> dbb10ff116f9b953e828e58703725fa63003cdfa
        while True:
            # draw screen
            self.screen.fill((255, 255, 255))
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
                    for i in range(len(TOWERS)):
                        if event.type == pygame.USEREVENT + i + 2:
                            TOWERS[i].action = True

<<<<<<< HEAD

=======
            # do tower action
            for tower_index in range(len(TOWERS)):
                pass
>>>>>>> dbb10ff116f9b953e828e58703725fa63003cdfa

    def toggle_pause(self):
        self.paused = not self.paused

    def test(self):
        A = Balloon_unit()
        A.set(1)
        BALLOONS.append(A)
        while True:
            # draw screen
            self.screen.fill((255, 255, 255))
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
        pass

if __name__ == '__main__':
    TD = TD_App()
    TD.test()


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
