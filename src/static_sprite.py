import pygame as py

class loaded_sprite(py.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

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
            self.pos[0] -= offset
        if where == "L":
            self.pos[0] += offset
        if where == "U":
            self.pos[1] += offset
        if where == "D":
            self.pos[1] -= offset
        self.rect.topleft = self.pos
    
    def set_size(self, size):
        self.image = py.transform.scale(self.image, size)
