#!/usr/bin/python3.6
#coding:utf-8

import time,pygame
from pygame.locals import *

class Basic(object):
    def __init__(self,location,screen,image):
        self.location = location
        self.screen = screen
        self.image = image
    def display(self):
        self.screen.blit(self.image,(self.location[0],self.location[1]))
#--------------------------------
class Jump_element(Basic):
    def __init__(self,name,location,screen,image):
        super().__init__(location,screen,image)
        self.name = name

class Attack_basic(Basic):
    def __init__(self,name,hp,at,location,screen,image):
        super().__init__(location,screen,image)
        self.name = name
        self.hp = hp
        self.at = at
    def attack(self,enermy):
        enermy.hp -= self.at
#--------------------------------
class Glass(Basic):
    def __init__(self,location,screen):
        super().__init__(location,screen,pygame.image.load("./resource/glass.png"))

class Stone(Basic):
    def __init__(self,location,screen):
        super().__init__(location,screen,pygame.image.load("./resource/stone.png"))
#--------------------------------
class Player(Attack_basic):
    def __init__(self,name,locate_at,hp,at,location,screen):
        super().__init__(name,hp,at,location,screen,pygame.image.load("./resource/player.png"))
        self.locate_at = locate_at

    def move_up(self):
        self.location[1] -= 20
    def move_down(self):
        self.location[1] += 20
    def move_left(self):
        self.location[0] -= 20
    def move_right(self):
        self.location[0] += 20

class Moster(Attack_basic):
    def __init__(self,name,hp,at,location,screen):
        super().__init__(name,hp,at,location,screen,pygame.image.load("./resource/moster.png"))

class Maps(object):
    def __init__(self,map_name,*element_list):
        self.map_name = map_name
        self.element_list = element_list
    def display(self):
        for i in self.element_list:
            for j in i:
                j.display()

#-------------------------------------------------
def town_element_index(element_type):
    if element_type == "glass":
        return [(20*x,20*y) for x in range(20) for y in range(20)]
    elif element_type == "stone":
        return [(20*x,0) for x in range(20) if x%2==1]
    elif element_type == "dong_fu":
        return [(0,0)]
    elif element_type == "ji_shi":
        return [(40,0)]
    elif element_type == "dead_place":
        return [(80,0)]

def dead_place_element_index(element_type):
    if element_type == "glass":
        return [(20*x,20*y) for x in range(20) for y in range(20)]
    elif element_type == "stone":
        return [(20,20*y) for y in (16,18,19)]+[(40,340)]
    elif element_type == "tiger_moutain":
        return [(20,340)]
    elif element_type == "exit":
        return [(0,380)]

def tiger_moutain_element_index(element_type):
    if element_type == "glass":
        return [(20*x,20*y) for x in range(20) for y in range(20)]
    elif element_type == "stone":
        return [(20,20*y) for y in range(2,8)]+[(20*x,160) for x in range(1,6)]+[(180,20*y) for y in range(3,12)]+[(20*x,200) for x in [10,11,12]]
    elif element_type == "exit":
        return [(0,380)]
    
def generate_element(element_type,index,screen):
    if element_type == "glass":
        return [Glass(x,screen) for x in index]
    elif element_type == "stone":
        return [Stone(x,screen) for x in index]
    elif element_type == "dong_fu":
        return [Jump_element("dong_fu",x,screen,pygame.image.load("./resource/dong_fu.png")) for x in index]
    elif element_type == "ji_shi":
        return [Jump_element("ji_shi",x,screen,pygame.image.load("./resource/ji_shi.png")) for x in index]
    elif element_type == "dead_place":
        return [Jump_element("dead_place",x,screen,pygame.image.load("./resource/dead_place.png")) for x in index]
    elif element_type == "tiger_moutain":
        return [Jump_element("tiger_moutain",x,screen,pygame.image.load("./resource/tiger_moutain.png")) for x in index]
    elif element_type == "exit":
        return [Jump_element("exit",x,screen,pygame.image.load("./resource/exit.png")) for x in index]
#-------------------------------------------------
def key_control(player,move_flags):
    for event in pygame.event.get():
        if event.type == QUIT:
            print("exit")
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_w:
                if move_flags[0] == 0:
                    if player.location[1] > 0:
                        player.move_up()
            elif event.key == K_s:
                if move_flags[1] == 0:
                    if player.location[1] < 380:
                        player.move_down()
            elif event.key == K_a:
                if move_flags[2] == 0:
                    if player.location[0] > 0:
                        player.move_left()
            elif event.key == K_d:
                if move_flags[3] == 0:
                    if player.location[0] < 380:
                        player.move_right()

def map_flags(player,current_map):
    up_flag = 0
    down_flag = 0
    left_flag = 0
    right_flag = 0
    jump_flag = 0
    jump_element = None
    attack_flag = 0
    moster_element = None
    for i in current_map.element_list:
        for j in i:
            if isinstance(j,Stone):
                if player.location[0] == j.location[0]:
                    if (player.location[1]-20) == j.location[1]:
                        up_flag = 1
                    if (player.location[1]+20) == j.location[1]:
                        down_flag = 1
                if player.location[1] == j.location[1]:
                    if (player.location[0]-20) == j.location[0]:
                        left_flag = 1
                    if (player.location[0]+20) == j.location[0]:
                        right_flag = 1
            elif isinstance(j,Jump_element):
                if player.location[0] == j.location[0] and player.location[1] == j.location[1]:
                    jump_flag = 1
                    jump_element = j
            elif isinstance(j,Moster):
                if player.location[0] == j.location[0] and player.location[1] == j.location[1]:
                    attack_flag = 1
                    moster_element = j

    return (up_flag,down_flag,left_flag,right_flag),(jump_flag,jump_element),(attack_flag,moster_element)
def jump_map(player,flags):
    if flags[0] == 1:
        if flags[1].name == "exit":
            if player.locate_at == "dead_place":
                player.locate_at = "town"
                player.location = [80,20]
                return
            if player.locate_at == "tiger_moutain":
                player.locate_at = "dead_place"
                player.location = [0,340]
                return
            if player.locate_at == "snake_lake":
                player.locate_at = "dead_place"
                player.location = [0,300]
                return
            if player.locate_at == "fox_hole":
                player.locate_at = "dead_place"
                player.location = [0,260]
                return
        else: 
            player.locate_at = flags[1].name
            player.location = [0,360]
            print(player.locate_at)

def attack_moster(flags):
    pass

def operation(player,current_map): 
    flags = map_flags(player,current_map)
    key_control(player,flags[0])
    jump_map(player,flags[1])
    attack_moster(flags[2])

def town_map(screen):
    glass = "glass"
    stone = "stone"
    dong_fu = "dong_fu"
    ji_shi = "ji_shi"
    dead_place = "dead_place"

    glass_index = town_element_index(glass)    #glass index
    town_stone_index = town_element_index(stone)  #town_stone_index
    town_dong_fu_index = town_element_index(dong_fu)
    town_ji_shi_index = town_element_index(ji_shi)
    town_dead_place_index = town_element_index(dead_place)

    glass_list = generate_element(glass,glass_index,screen)
    town_stone_list = generate_element(stone,town_stone_index,screen)
    town_dong_fu_list = generate_element(dong_fu,town_dong_fu_index,screen)
    town_ji_shi_list = generate_element(ji_shi,town_ji_shi_index,screen)
    town_dead_place_list = generate_element(dead_place,town_dead_place_index,screen)

    return Maps("town",glass_list,town_stone_list,town_dong_fu_list,town_ji_shi_list,town_dead_place_list)

def dead_place_map(screen):
    glass = "glass"
    stone = "stone"
    tiger_moutain = "tiger_moutain"
    exit = "exit"

    glass_index = town_element_index(glass)
    dead_place_stone_index = dead_place_element_index(stone)
    dead_place_tiger_moutain_index = dead_place_element_index(tiger_moutain)
    dead_place_exit_index = dead_place_element_index(exit)

    glass_list = generate_element(glass,glass_index,screen)
    dead_place_stone_list = generate_element(stone,dead_place_stone_index,screen)
    dead_place_tiger_moutain_list = generate_element(tiger_moutain,dead_place_tiger_moutain_index,screen)
    dead_place_exit_list = generate_element(exit,dead_place_exit_index,screen)

    return Maps("dead_place",glass_list,dead_place_stone_list,dead_place_tiger_moutain_list,dead_place_exit_list)

def tiger_moutain_map(screen):
    glass = "glass"
    stone = "stone"
    exit = "exit"

    glass_index = town_element_index(glass)
    tiger_moutain_stone_index = tiger_moutain_element_index(stone)
    tiger_moutain_exit_index = tiger_moutain_element_index(exit)

    glass_list = generate_element(glass,glass_index,screen)
    tiger_moutain_stone_list = generate_element(stone,tiger_moutain_stone_index,screen)
    tiger_moutain_exit_list = generate_element(exit,tiger_moutain_exit_index,screen)

    return Maps("tiger_moutain",glass_list,tiger_moutain_stone_list,tiger_moutain_exit_list)

def main():
    #screen = pygame.display.set_mode((400,400),0,32)
    #background = pygame.image.load("xx.png")
    #screen.blit(background,(x,y))
    #pygame.display.update()
    screen = pygame.display.set_mode((400,400),0,32)
    player = Player("sam","town",100,5,[0,40],screen)
    
    while True:
        if player.locate_at == "town":
            current_map = town_map(screen)
        elif player.locate_at == "dead_place":
            current_map = dead_place_map(screen)
        elif player.locate_at == "tiger_moutain":
            current_map = tiger_moutain_map(screen)
        current_map.display()
        player.display()
        operation(player,current_map)
        pygame.display.update()
        time.sleep(0.01)

if __name__=="__main__":
    main()
