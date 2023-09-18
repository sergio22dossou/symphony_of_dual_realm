#!/usr/bin/env python3

import pygame as py
import os
import random

class many_static(py.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, where, offset):
        if where == "R":
            self.pos[0] += offset
        if where == "L":
            self.pos[0] -= offset
        if where == "U":
            self.pos[1] -= offset
        if where == "D":
            self.pos[1] += offset
        self.rect.topleft = self.pos
    
    def set_size(self, size):
        self.image = py.transform.scale(self.image, size)

class static_sprite(py.sprite.Sprite):
    def __init__(self, file_name, pos):
        super().__init__()
        self.file = file_name
        self.pos = pos
        self.image = py.image.load(file_name)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, where, offset):
        if where == "R":
            self.pos[0] += offset
        if where == "L":
            self.pos[0] -= offset
        if where == "U":
            self.pos[1] -= offset
        if where == "D":
            self.pos[1] += offset
        self.rect.topleft = self.pos
    
    def set_size(self, size):
        self.image = py.transform.scale(self.image, size)

class animd_sprite(py.sprite.Sprite):
    def __init__(self, dir_name, pos, inc_speed, max_size, offset):
        super().__init__()
        self.dir_name = dir_name
        self.current = 0
        self.pos = pos
        self.inc_speed = inc_speed
        self.max = max_size
        self.offset = offset
        self.dir = dir_name
        list_img = os.listdir(dir_name)
        list_img.sort()
        self.imgs = []
        for img in list_img:
            self.imgs.append(py.image.load(f'{self.dir}/{img}'))
        self.image = self.imgs[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    
    def update(self, offset):
        if (self.offset != offset):
            self.offset = offset
            self.current = offset
        self.current += self.inc_speed
        if (int(self.current) > (self.max + offset)):
            self.current = self.offset
        self.image = self.imgs[int(self.current)]

    def move(self, where, offset):
        if where == "R":
            self.pos[0] += offset
        if where == "L":
            self.pos[0] -= offset
        if where == "U":
            self.pos[1] -= offset
        if where == "D":
            self.pos[1] += offset
        self.rect.topleft = self.pos
    
    def set_size(self, size):
        i = 0
        while i < len(self.imgs):
            self.imgs[i] = py.transform.scale(self.imgs[i], size)
            i += 1
        self.rect.size = size

class level_body: #this represent the design of the level create from a file
    def __init__(self, file_name):
        stri = ''
        with open(file_name, "r") as map:
            stri = map.read()
        self.map = stri.split('\n', stri.count('\n'))

# class score: #this is the score an increase and decrease function to carry the score
#     def __init__(self, score):
#         self.score = score
    
#     def increase(self, offset):
#         self.score += offset
    
#     def decrease(self, offset):
#         self.score -= offset

class player(animd_sprite):
     def __init__(self, dir_name, pos, inc_speed, max_size, offset, life, pv, inventory):
         super().__init__(dir_name, pos, inc_speed, max_size, offset)
         self.life = life
         self.pv = pv
         self.inventory = inventory

# class badguy:
#     def __init__(self, pos, bg_file, life, inventory, rect):
#         self.life = life

class level:
    def __init__(self, window, surface, level, key, scale, group, key_grp, static):
        self.surface = surface
        self.key = key
        self.scale = scale
        self.level = level_body(level+"/ted.txt")
        self.group = group
        self.key_grp = key_grp
        self.static = static
        self.state = 0
        self.sound = py.mixer.Sound(f'./{level}/{level}.ogg')
        self.sound.play(-1)

    def loading_img(self):
        self.img_keys = {}
        for elem in self.key:
            spr = py.image.load(self.key[elem])
            self.img_keys[elem] = spr

    def init_group(self):
        self.dec = [0,0]
        self.path = py.sprite.Group()
        self.decor = py.sprite.Group()
        self.dynamc_obj = py.sprite.Group()
        self.png = py.sprite.Group()
        self.enemy = py.sprite.Group()
        self.anex = py.sprite.Group()
        self.lucas = player("./lvl1/Lucas", [250, 300], 0.09, 2, 0, 3, 50, [])
        self.lucas.rect.size = (41, 41)
        # self.bg = static_sprite(self.key[' '], [0, 0])
        # self.bg.image = py.transform.scale(self.bg.image, self.scale[' '])
        # self.tr = static_sprite(self.key['t'], [0, 0])
        # self.tr.image = py.transform.scale(self.tr.image, self.scale['t'])

    def init_map(self):
        self.init_group()
        x, y = 0, 0
        self.loading_img()
        for line in self.level.map:
            x = 0
            for elem in line:
                spr = static_sprite(self.key[' '], [x, y])
                spr.image = py.transform.scale(spr.image, self.scale[' '])
                self.path.add(spr)
                if elem in self.img_keys and elem != ' ':
                    spr = many_static(self.img_keys[elem], [x, y])
                    spr.image = py.transform.scale(spr.image, self.scale[elem])
                    spr.rect.size = self.scale[elem]
                    tmp = getattr(self, self.key_grp[elem])
                    tmp.add(spr)
                x += 50
            y += 50

    def is_inter(self, vlue, a, b):
        if (vlue > a and vlue < b):
            return True
        else:
            return False

    def detect(self, rec1, rec2, move):
        pos1, pos2 = rec1.topleft, rec2.topleft
        s1, s2 = rec1.size, rec2.size
        if (move == 'D' and pos1[1] < pos2[1] and pos1[0] < pos2[0]+s2[0]-9):
            return True
        if (move == 'U' and pos1[1] > pos2[1] and pos1[0] < pos2[0]+s2[0]-9):
            return True
        if (move == 'R' and pos1[0] < pos2[0]
            and (self.is_inter(pos1[1], pos2[1], pos2[1]+s2[1]-7) or
            self.is_inter(pos2[1], pos1[1], pos1[1]+s1[1]-7))):
            return True
        if (move == 'L' and pos1[0] > pos2[0] and
            ( self.is_inter(pos1[1], pos2[1], pos2[1]+s2[1]-7) or
            self.is_inter(pos2[1], pos1[1], pos1[1]+s1[1]-7))):
            return True
        return False

    def is_colliding(self, perso, grp, move):
        for elem in grp:
            if (perso.rect.colliderect(elem.rect) and 
                self.detect(perso.rect, elem.rect, move)):
                return True
        return False
    
    def parralax(self, pos, offset):
        self.path.update(pos, offset)
        self.decor.update(pos, offset)
        self.dynamc_obj.update(pos, offset)
        self.enemy.update(pos, offset)

    def play_move(self):
        key = py.key.get_pressed()
        if key[py.K_RIGHT] and self.is_colliding(self.lucas, self.decor, 'R') == False:
            self.dec[0] += -2
            self.parralax('R', -2)
            self.state = 6
        elif key[py.K_LEFT] and self.is_colliding(self.lucas, self.decor, 'L') == False:
            self.parralax('L', -2)
            self.dec[0] += 2
            self.state = 3
        elif key[py.K_UP] and self.is_colliding(self.lucas, self.decor, 'U') == False:
            self.parralax('U', -2)
            self.state = 9
        elif key[py.K_DOWN] and self.is_colliding(self.lucas, self.decor, 'D') == False:
            self.parralax('D', -2)
            self.state = 0

    def draw_map(self):
        self.path.draw(self.surface)
        self.decor.draw(self.surface)
        self.dynamc_obj.draw(self.surface)
        self.png.draw(self.surface)
        self.enemy.draw(self.surface)
        self.anex.draw(self.surface)

    def draw_bg(self):
        x, y = self.dec
        for line in self.level.map:
            x = 0
            for elem in line:
                self.bg.rect.topleft = [x+self.dec[0], y]
                self.surface.blit(self.bg.image, self.bg.rect)
                x += 50
            y += 50
        x, y = self.dec
        for line in self.level.map:
            x = 0
            for elem in line:
                if elem == 't':
                    self.tr.rect.topleft = [x+self.dec[0], y]
                    self.surface.blit(self.tr.image, self.tr.rect)
                x += 50
            y += 50

    def run(self):
        self.surface.fill((0, 0, 0))
        #self.draw_bg()
        self.lucas.update(self.state)
        self.draw_map()
        self.surface.blit(self.lucas.image, self.lucas.rect)
        self.play_move()