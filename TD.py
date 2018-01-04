import pygame
import sys

# constants
MAP_INDEX = 0
ROAD_INDEX = 1

screen_size = 1000, 700

# RGBA color
colors = {
    (14, 209, 69, 255),
    (185, 122, 86, 255)
}

map_img = pygame.image.load("map1.png")
map_rect = map_img.get_rect()


class Unit(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0


class Tower_unit(Unit):
    def __init__(self):
        super().__init__()
        self.attack_damage = 0
        self.attack_range = 0
        self.expense = 0
        self.action = False

    def set(self, n):
        pass
        # self.action - data[n][4]

    def upgrade(self):
        pass


class Balloon_unit(Unit):
    def __init__(self):
        super().__init__()
        self.reward = 0
        self.life = 0
        self.speed = 0
        self.level = 0  # speed, life depends on balloon level


class Map(object):
    def __init__(self):
        pygame.init()
        self.width = 1000
        self.height = 700
        self.road_width = 50
        map = pygame.Surface((self.width, self.height))


class TD_App(object):
    def __init__(self):
        # pygame setting
        pygame.init()
        # self.default_font = pygame.font.Font(
        #     pygame.font.get_default_font(), 12
        # )

        # screen setting
        self.screen = pygame.display.set_mode(screen_size)

        # money to install unit
        self.budget = 0
        # If life == 0 --> gameover
        self.life = 0

        # define self variable
        self.gameover = False
        self.paused = False
        self.num_tower = 0

    def road(self):
        pass
        self.towers = []

    def run(self):
        key_actions = {
            'ESCAPE': sys.exit,
            'p': self.toggle_pause
        }
        while True:
            # draw screen
            self.screen.fill((255, 255, 255))
            self.screen.blit(map_img, map_rect)
            for i in range(self.num_tower):
                self.draw_unit(self.towers[i])
                pass
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

            # for i in range(self.num_tower):
            #     target = self.find_target(i)
            #     # do action

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