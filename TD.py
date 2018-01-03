import pygame
import sys

# data set
# width = 0
# height = 1
# attack_damage = 2
# attack_range = 3
data = [
    [50, 30, 10, 50],
    [40, 60, 20, 60],
    [50, 50, 30, 70]
]

screen_size = 400, 300


class Tower_unit(object):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.attack_damage = 0
        self.attack_range = 0

    def set(self, n):
        self.width = data[n][0]
        self.height = data[n][1]
        self.attack_damage = data[n][2]
        self.attack_range = data[n][3]


class Wandering_unit(object):
    pass


class TD_App(object):
    def __init__(self):
        # pygame setting
        pygame.init()
        self.default_font = pygame.font.Font(
            pygame.font.get_default_font(), 12
        )

        # screen setting
        self.screen = pygame.display.set_mode(screen_size)

        # define self variable
        self.num_tower = 0


    def run(self):
        while True:
            # draw screen
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                else:
                    for i in range(1, self.num_tower):
                        if event.type == pygame.USEREVENT + i:
                            #towers(i).action()
                            pass


