#coding:utf-8
#/usr/bin/python3

import time,pygame
from pygame.locals import *

class Basic(object):
    def __init__(self,location,screen,element):
        self.location = location
        self.screen = screen
        self.element = element

    def display(self):
        self.screen.blit(self.element,(self.location[0],self.location[1]))

class Player(Basic):
    def __init__(self,name,location,screen):
        super().__init__(location,screen,pygame.image.load("./resource/player.png"))
        self.name = name

    def move_up(self):
        self.location[1] -= 20
    def move_down(self):
        self.location[1] += 20
    def move_left(self):
        self.location[0] -= 20
    def move_right(self):
        self.location[0] += 20
    def attack(self,moster):
        print("attacking")

class Moster(Basic):
    def __init__(self,name,location,screen):
        super().__init__(location,screen,pygame.image.load("./resource/moster.png"))
        self.name = name

class Stone(Basic):
    def __init__(self,location,screen):
        super().__init__(location,screen,pygame.image.load("./resource/stone.png"))

class Glass(Basic):
    def __init__(self,location,screen):
        super().__init__(location,screen,pygame.image.load("./resource/glass.png"))

class Relive_Warter(Basic):
    def __init__(self,location,screen):
        super().__init__(location,screen,pygame.image.load("./resource/relive_warter.png"))



class Maps(object):
    def __init__(self,*element_list):      #传入地图中所有的元素的列表,列表的列表
        self.element_list = element_list

    def display(self):
        for i in self.element_list:
            for j in i:
                j.display()

#-----------glass元素对象-------------------#
def glass_all(screen,map_index):
    return [Glass(x,screen) for x in map_index]

#------------tiger_moutain------------#    
def tiger_moutain_stone(screen,stone_index):
    return [Stone(x,screen) for x in stone_index]

def tiger_moutain_moster(screen,moster_index):
    return [Moster("tiger_moster",x,screen) for x in moster_index]

#------------------------------------------------------#


#------汇总map中无法到达的坐标列表
def maps_can_not_move_element_list(*args):
    sum_can_not_move_to_element = []
    for i in args:
        sum_can_not_move_to_element +=i
    return sum_can_not_move_to_element


def judge_can_not_move(key_down,player,element_list):
    can_not_up_flag = 0
    can_not_down_flag = 0
    can_not_left_flag = 0
    can_not_right_flag = 0
    if key_down == "up":
        for i in element_list:
            if player.location[0] == i.location[0]:
                if (player.location[1]-20) == i.location[1]:
                    can_not_up_flag = 1
                    break
    if key_down == "down":
        for i in element_list:
            if player.location[0] == i.location[0]:
                if (player.location[1]+20) == i.location[1]:
                    can_not_down_flag = 1
                    break
    if key_down == "left":
        for i in element_list:
            if player.location[1] == i.location[1]:
                if (player.location[0]-20) == i.location[0]:
                    can_not_left_flag = 1
                    break
    if key_down == "right":
        for i in element_list:
            if player.location[1] == i.location[1]:
                if (player.location[0]+20) == i.location[0]:
                    can_not_right_flag = 1
                    break
    return can_not_up_flag,can_not_down_flag,can_not_left_flag,can_not_right_flag
    
def judge_hit(player,element_list):
    moster_flag = 0
    for i in element_list:
        if player.location[0] == i.location[0] and player.location[1] == i.location[1]:
            moster_flag =1
            moster = i
            break
    if moster_flag == 1:
        return moster

def key_control(player,stone_list,moster_list):
    for event in pygame.event.get():
        if event.type == QUIT:
            print("exit")
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_w:
                stone_up_flag = judge_can_not_move("up",player,stone_list)
                if stone_up_flag[0] == 0:
                    if player.location[1] > 0:
                        print("上")
                        player.move_up()
            elif event.key == K_s:
                stone_down_flag = judge_can_not_move("down",player,stone_list)
                if stone_down_flag[1] == 0:
                    if player.location[1] < 380:
                        print("下")
                        player.move_down()
            elif event.key == K_a:
                stone_left_flag = judge_can_not_move("left",player,stone_list)
                if stone_left_flag[2] == 0:
                    if player.location[0] > 0:
                        print("左")
                        player.move_left()
            elif event.key == K_d:
                stone_right_flag = judge_can_not_move("right",player,stone_list)
                if stone_right_flag[3] == 0:
                    if player.location[0] < 380:
                        print("右")
                        player.move_right()
            moster = judge_hit(player,moster_list)
            if moster:
                player.attack(moster)
        
def main():
    screen = pygame.display.set_mode((400,400),0,32)
    player = Player("sam",[0,380],screen)

    map_index = [(20*x,20*y) for x in range(20) for y in range(20)]
    tiger_moutain_stone_index = [(20,20*y) for y in range(1,7)] + [(20,20*y) for y in range(8,20)] + [(20*x,160) for x in range(2,6)] + [(20*x,120) for x in range(11,15)] + [(200,20*y) for y in range(6,15)] + [(20*x,200) for x in range(13,20)]
    tiger_moutain_moster_index = [(160,140),(240,300)]

    glass_list = glass_all(screen,map_index)
    tiger_moutain_stone_list = tiger_moutain_stone(screen,tiger_moutain_stone_index)
    tiger_moutain_moster_list = tiger_moutain_moster(screen,tiger_moutain_moster_index)
    #tiger_moutain_can_not_move_element_list = maps_can_not_move_element_list(tiger_moutain_stone_list)
    tiger_moutain = Maps(glass_list,tiger_moutain_stone_list,tiger_moutain_moster_list)

    while True:
        tiger_moutain.display()
        player.display()
        key_control(player,tiger_moutain_stone_list,tiger_moutain_moster_list)
        pygame.display.update()
        time.sleep(0.01)


if __name__ == "__main__":
    main()
