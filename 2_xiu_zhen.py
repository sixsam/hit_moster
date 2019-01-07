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


class AttackBasic(Basic):
    def __init__(self,name,at,hp,location,screen,image):
        super().__init__(location,screen,image)
        self.name = name
        self.at = at
        self.hp = hp
    def attack(self,item):
        item.hp -= self.at
        print("%s attack %s ,%s lose %d blood."%(self.name,item.name,item.name,self.at))


class Player(AttackBasic):
    def __init__(self,name,location,screen,at=5,hp=100,experience=0,level=1):
        super().__init__(name,at,hp,location,screen,pygame.image.load("./resource/player.png"))
        self.experience = experience
        self.level = level
    def move_up(self):
        self.location[1] -= 20
    def move_down(self):
        self.location[1] += 20
    def move_left(self):
        self.location[0] -= 20
    def move_right(self):
        self.location[0] += 20


class Moster(AttackBasic):
    def __init__(self,name,at,hp,location,screen):
        super().__init__(name,at,hp,location,screen,pygame.image.load("./resource/moster.png"))

class Tiger_moster(Moster):
    def __init__(self,at,hp,location,screen):
        super().__init__(at,hp,location,screen,name="tiger_moster")

class Snake_moster(Moster):
    def __init__(self,at,hp,location,screen):
        super().__init__(at,hp,location,screen,name="snake_moster")

class Fox_moster(Moster):
    def __init__(self,at,hp,location,screen):
        super().__init__(at,hp,location,screen,name="fox_moster")


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
    def __init__(self,*element_list):      #传入地图中元素的所有列表
        self.element_list = element_list

    def display(self):
        for i in self.element_list:
            for j in i:
                if isinstance(j,Moster):
                    if j.hp > 0:
                        j.display()
                else:
                    j.display()

#-----------glass元素对象-------------------#
def glass_all(screen,map_index):
    return [Glass(x,screen) for x in map_index]

#------------生成小元素对象------------#    
def map_stone(screen,stone_index):
    return [Stone(x,screen) for x in stone_index]

def map_moster(name,at,hp,screen,moster_index):
    return [Moster(name,at,hp,x,screen) for x in moster_index]

#------------------------------------------------------#


#------汇总map中同类对象
def sum_class_element_list(*args):
    sum_class_element = []
    for i in args:
        sum_class_element +=i
    return sum_class_element


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
    
def judge_hit(player,moster_list):
    moster_flag = 0
    for i in moster_list:
        if player.location[0] == i.location[0] and player.location[1] == i.location[1]:
            moster_flag =1
            moster = i
            break
    if moster_flag == 1:
        return moster

def attacking(player,moster):
    while True:
        print(moster.hp)
        print(player.hp)
        if moster.hp <= 0:
            print("you kill a %s"%moster.name)
            player.experience += 20
            if player.experience // player.level ==120:
                player.level +=1
            player.hp = 100
            break
        if player.hp <= 0:
            print("you are kill by %s"%moster.name)
            break
        player.attack(moster)
        moster.attack(player)
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
                attacking(player,moster)
        
def main():
    screen = pygame.display.set_mode((400,400),0,32)
    player = Player("sam",[0,380],screen)

    map_index = [(20*x,20*y) for x in range(20) for y in range(20)]
    tiger_moutain_stone_index = [(20,20*y) for y in range(1,7)] + [(20,20*y) for y in range(8,20)] + [(20*x,160) for x in range(2,6)] + [(20*x,120) for x in range(11,15)] + [(200,20*y) for y in range(6,15)] + [(20*x,200) for x in range(13,20)]
    tiger_moutain_tiger_moster_index = [(160,140),(240,300)]
    tiger_moutain_snake_moster_index = [(240,80),(60,340)]

    glass_list = glass_all(screen,map_index)
    tiger_moutain_stone_list = map_stone(screen,tiger_moutain_stone_index)
    tiger_moutain_tiger_moster_list = map_moster("tiger_moster",5,20,screen,tiger_moutain_tiger_moster_index)
    tiger_moutain_snake_moster_list = map_moster("snake_moster",5,20,screen,tiger_moutain_snake_moster_index)
    tiger_moutain_moster_element_list = sum_class_element_list(tiger_moutain_tiger_moster_list,tiger_moutain_snake_moster_list)
    tiger_moutain = Maps(glass_list,tiger_moutain_stone_list,tiger_moutain_moster_element_list)

    while True:
        tiger_moutain.display()
        player.display()
        key_control(player,tiger_moutain_stone_list,tiger_moutain_moster_element_list)
        pygame.display.update()
        time.sleep(0.01)


if __name__ == "__main__":
    main()
