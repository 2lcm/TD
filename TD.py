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

screen_size = 1000, 700


class Tower_unit(object):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.attack_damage = 0
        self.attack_range = 0
        self.action = False

    def set(self, n):
        self.width = data[n][0]
        self.height = data[n][1]
        self.attack_damage = data[n][2]
        self.attack_range = data[n][3]
        # self.action - data[n][4]


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
        self.gameover = False
        self.paused = False
        self.num_tower = 0
        self.towers = []

    def run(self):
        key_actions = {
            'EXCAPE': sys.exit,
            'p': self.toggle_pause
        }
        while True:
            # draw screen
            self.screen.fill((255, 255, 255))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_" + key):
                            key_actions[key]()
                else:
                    for i in range(self.num_tower):
                        if event.type == pygame.USEREVENT + i + 1:
                            self.towers[i].action = True

            for i in range(self.num_tower):
                target = self.find_target(i)
                # do action

    def toggle_pause(self):
        self.paused = not self.paused

    def find_target(self, tower_index):
        #towers[tower_index]
        target = None
        return target