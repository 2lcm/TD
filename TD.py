import pygame
import sys
import numpy as np
import time

# pygame.USEREVENT list
# USEREVENT + 1 : balloon generating timer
# USEREVENT + (i + 2) : attacking timer of towers[i]

# constants
SCREEN_SIZE = 1000, 700
ROAD_WIDTH = 70
MAP_INDEX = 0
ROAD_INDEX = 1
STARTING_POINT = 0, 500

# RGBA color
colors = {
    (14, 209, 69, 255),
    (185, 122, 86, 255)
}

TOWERS = []
BALLOONS = []
DARTS = []
TIMER = []

# Index | meaning(?)
# 0 :
database = []

map_img = pygame.image.load("map1.png")
map_rect = map_img.get_rect()

balloon_img = pygame.image.load("balloon.png")
balloon_img = pygame.transform.scale(balloon_img, (ROAD_WIDTH, ROAD_WIDTH))

tower_img = pygame.image.load("tower.png")
tower_img = pygame.transform.scale(tower_img, (ROAD_WIDTH, ROAD_WIDTH))


class Unit(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = []
        self.rect = None

    def move(self):
        self.rect.center = self.x + self.speed[0], self.y + self.speed[1]


class Tower_unit(Unit):
    def __init__(self):
        super().__init__()
        self.attack_range = 0
        #self.expense = 0
        self.action = False

    def position(self):
        return (self.x, self.y)


class Balloon_unit(Unit):
    def __init__(self):
        super().__init__()
        #self.reward
        self.level = 0  # speed, life depends on balloon level

    def set(self, level):
        self.x, self.y = STARTING_POINT
        pygame.Rect(self.x, self.y, ROAD_WIDTH, ROAD_WIDTH)
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
        self.towers = []
        self.balloons = []

    def draw_unit(self, unit):
        pass

    def run(self):
        key_actions = {
            'ESCAPE': sys.exit,
            'p': self.toggle_pause
        }

        temp_balloon = Balloon_unit()
        temp_tower = Tower_unit()
        tower_rect.center = temp_tower.position()
        while True:
            # draw screen
            self.screen.fill((255, 255, 255))
            self.screen.blit(map_img, map_rect)
            self.screen.blit(tower_img, tower_rect)
            for i in range(len(self.towers)):
                self.draw_unit(self.towers[i])
                pass

            # print(temp_balloon.move())
            # temp_tower.attack(temp_balloon.move()[0], temp_balloon.move()[1])

            self.screen.blit(balloon_img, balloon_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_" + key):
                            key_actions[key]()
                else:
                    for i in range(len(self.towers)):
                        if event.type == pygame.USEREVENT + i + 2:
                            self.towers[i].action = True

            for i in range(len(self.towers)):
                target = self.find_target(i)
                # do action

            for i in range(len(self.balloons)):
                self.balloons[i].center =

            balloon_rect.center = temp_balloon.move()

    def toggle_pause(self):
        self.paused = not self.paused

    def find_target(self, tower_index):
        #towers[tower_index]
        target = None
        return target

    def test(self):
        pass


if __name__ == '__main__':
    TD = TD_App()
    TD.run()


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
