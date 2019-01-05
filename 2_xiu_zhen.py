#coding:utf-8
#/usr/bin/python3

import time,pygame

class Element_basic(object):
    def __init__(self,location,screen):
        self.x = location[0]
        self.y = location[1]
        self.screen = screen

    def display(self):
        self.screen.blit(self.element,(self.x,self.y))

class Stone(Element_basic):
    def __init__(self,location,screen):
        super().__init__(location,screen)
        self.element = pygame.image.load("./resource/stone.png")

class Glass(Element_basic):
    def __init__(self,location,screen):
        super().__init__(location,screen)
        self.element = pygame.image.load("./resource/glass.png")

class Maps(object):
    def __init__(self,name,element_list):
        self.name = name
        self.element_list = element_list

    def display(self):
        for i in self.element_list:
            i.display()

def snake_gu():
    pass

def town():
    pass

def tiger_moutain(screen):
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
