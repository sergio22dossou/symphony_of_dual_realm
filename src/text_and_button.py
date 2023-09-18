#!/usr/bin/env python3

import pygame as py

class text(py.font.Font):
    def __init__(self, font, text, color, size):
        self.font = super().__init__(font, size)
        self.text = text
        self.color = color

    def draw(self, screen, pos):
        i = 0
        j = 0
        tmp = self.text.split('\n', self.text.count('\n'))
        for line in tmp:
            img = self.render(line, True, self.color)
            self.rect = img.get_rect()
            self.rect.topleft = pos
            screen.blit(img, self.rect)
            pos[1] += 40

    def update(self, txt):
        self.text = txt

class button(py.sprite.Sprite):
    def __init__(self, path, pos, size):
        super().__init__()
        self.img = py.image.load(path)
        self.rect = self.img.get_rect()
        self.rect.topleft = pos
        self.rect.size = size
        self.img = py.transform.scale(self.img, size)
    
    def update(self, size):
        self.img = py.transform.scale(self.img, size)

    def is_clicked(self, pos):
        if (pos[0] > self.rect.topleft[0] and pos[0] < self.rect.topright[0]):
            if (pos[1] > self.rect.topleft[1] and pos[1] < self.rect.bottomleft[1]):
                return True
        return False