import pygame as py
import os

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

    def play(self, offset):
        if (self.offset != offset):
            self.offset = offset
            self.current = offset
        self.current += self.inc_speed
        if (int(self.current) > (self.max + offset)):
            self.current = self.offset
        self.image = self.imgs[int(self.current)]

    def update(self, where, offset):
        if where == "R":
            self.pos[0] -= offset
        if where == "L":
            self.pos[0] += offset
        if where == "U":
            self.pos[1] += offset
        if where == "D":
            self.pos[1] -= offset
        self.rect.topleft = self.pos
    
    def set_size(self, size):
        list_img = os.listdir(self.dir_name)
        list_img.sort()
        self.imgs = []
        for img in list_img:
            spr = py.image.load(f'{self.dir}/{img}')
            spr = py.transform.scale(spr, size)
            self.imgs.append(spr)
        self.rect.size = size