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
        self.img = path
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

    def set_pos(self, pos):
        self.rect.topleft = pos

    def set_des(self, text):
        self.txt = text

class listing_buttons():
    def __init__(self, state):
        self.menu = []
        self.state = state
        self.index = 0

    def new_button(self, img, pos, size):
        tmp = button(img, pos, size)
        self.menu.append(tmp)

    def draw(self, status, screen):
        if status not in self.state: return 1
        for elem in self.menu: screen.blit(elem.img, elem.rect)

    def bar_move_down(self, event, state):
        if len(self.menu) < 2: return 0
        if event.key == py.K_DOWN and state in self.state:
            tmp = self.menu[self.index]
            self.index += 1
            if self.index > len(self.menu)-1: self.index = 0
            tmp2 = self.menu[self.index]
            x1, y1 = tmp.rect.size
            x2, y2 = tmp2.rect.size
            tmp.update((x2, y2))
            tmp2.update((x1+50, y1+20))

    def bar_move_up(self, event, state):
        if len(self.menu) < 2: return 0
        if event.key == py.K_UP and state in self.state:
            tmp = self.menu[self.index]
            self.index -= 1
            if self.index < 0: self.index = len(self.menu) - 1
            tmp2 = self.menu[self.index]
            x1, y1 = tmp.rect.size
            x2, y2 = tmp2.rect.size
            tmp.update((x2, y2))
            tmp2.update((x1+50, y1+20))

    def restart_menu_bar(self, size):
        for i in self.menu: i.update(size)
        if len(self.menu) != 0:
            self.menu[0].update((size[0]+50, size[1]+20))
