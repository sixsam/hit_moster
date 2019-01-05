#coding:utf-8
#/usr/bin/python3

import time,pygame

class Player(object):
    def __init__(self,location,screen):
        self.x = location[0]
        self.y = location[1]
        self.screen = screen
        self.player = pygame.image.load("./resource/player.png")
    def display(self):
        self.screen.blit(self.player,(self.x,self.y))

class Moster(object):
    def __init__(self,location,screen):
        self.x = location[0]
        self.y = location[1]
        self.screen = screen
        self.moster = pygame.image.load("./resource/moster.png")
    def display(self):
        self.screen.blit(self.moster,(self.x,self.y))

class Stone(object):
    def __init__(self,location,screen):
        self.x = location[0]
        self.y = location[1]
        self.screen = screen
        self.stone = pygame.image.load("./resource/stone.png")
    def display(self):
        self.screen.blit(self.stone,(self.x,self.y))

class Glass(object):
    def __init__(self,location,screen):
        self.x = location[0]
        self.y = location[1]
        self.screen = screen
        self.glass = pygame.image.load("./resource/glass.png")
    def display(self):
        self.screen.blit(self.glass,(self.x,self.y))

class Relive_Warter(object):
    def __init__(self,location,screen):
        self.x = location[0]
        self.y = location[1]
        self.screen = screen
        self.relive_warter = pygame.image.load("./resource/relive_warter.png")
    def display(self):
        self.screen.blit(self.relive_warter,(self.x,self.y))

def snake_gu():
    pass

def town():
    pass

def tiger_moutain():
    map_index = [(20*x,20*y) for x in range(20) for y in range(20)]
    tiger_moutain_stone_index = [(20,20*y) for y in range(1,7)] + [(20,20*y) for y in range(8,20)] + [(20*x,160) for x in range(2,6)] + [(20*x,120) for x in range(11,15)] + [(200,20*y) for y in range(6,15)] + [(20*x,200) for x in range(13,20)]
    tiger_moutain_glass_index = [x for x in map_index if x not in tiger_moutain_stone_index]
    return [Stone(x,screen) for x in tiger_moutain_stone_index] + [Glass(x,screen) for x in tiger_moutain_glass_index]

def main():
    screen = pygame.display.set_mode((400,400),0,32)
    tiger_moutain_element_list = tiger_moutain(screen)
    while True:
        tiger_moutain = Maps("tiger_moutain",tiger_moutain_element_list)
        tiger_moutain.display()
        pygame.display.update()
        time.sleep(0.01)


if __name__ == "__main__":
    main()
