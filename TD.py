import pygame
import sys
import numpy as np
import time


# constants
SCREEN_SIZE = 1000, 700
ROAD_WIDTH = 70
MAP_INDEX = 0
ROAD_INDEX = 1


# RGBA color
colors = {
    (14, 209, 69, 255),
    (185, 122, 86, 255)
}

map_img = pygame.image.load("map1.png")
map_rect = map_img.get_rect()
balloon_img = pygame.image.load("balloon.png")
balloon_img = pygame.transform.scale(balloon_img, (70,70))
balloon_rect = balloon_img.get_rect()


dart_img = pygame.image.load("needle.png")
dart_img = pygame.transform.scale(dart_img, (10,10))
tower_img  = pygame.image.load("tower.png")
tower_img = pygame.transform.scale(tower_img, (70,70))
tower_rect = tower_img.get_rect()

TOWERS = []
BALLOONS = []
DARTS = []
TIMER = []

class Unit(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = []
        self.rect = None

class Dart_unit(Unit):
    def __init__(self, tower_index, target_index):
        super().__init__()
        self.x, self.y =  TOWERS[tower_index].x, TOWERS[tower_index].y
        self.speed = BALLOONS[target_index].x - self.x, BALLOONS[target_index].y - self.y
        self.rect = dart_img.get_rect()
        self.rect.center =  self.x, self.y

class Tower_unit(Unit):

    def __init__(self):
        super().__init__()
        self.attack_range = 0
        self.expense = 0
        self.action = False

    def position(self):
        return (self.x, self.y)

    def set(self, position):
        self.x, self.y = position
        self.attack_range = 500

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
#########################
## It is just for testing
# test_tower = Tower_unit()
# test_tower.attack()
#########################

class Balloon_unit(Unit):
    def __init__(self):
        super().__init__()
        self.reward = 0
        self.life = 1
        self.level = 0  # speed, life depends on balloon level
        self.live = True
        self.x = 0
        self.y = 500
    def move(self):
        time.sleep(0.01)
        if self.life == 0 :
            self.live = False
        if self.live ==True:
            if self.x < 250 and self.y ==500:
                self.x+=1
            elif  self.y >200:
                self.y-=1
            elif self.x < 1000:
                self.x+=1
            # if self.x == 1000:
            #     print("It's over")
        return (self.x, self.y)



#########################
## It is just for testing
# temp_balloon = Balloon_unit()
# temp_balloon.move()
#########################




class Map(object):
    def __init__(self):
        pass


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

    def road(self):
        pass

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
            print(temp_balloon.move())
            temp_tower.attack(temp_balloon.move()[0], temp_balloon.move()[1])


            balloon_rect.center = temp_balloon.move()
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
                        if event.type == pygame.USEREVENT + i + 1:
                            self.towers[i].action = True

            for i in range(len(self.towers)):
                target = self.find_target(i)
                # do action

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
