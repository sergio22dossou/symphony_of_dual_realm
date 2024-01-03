#!/usr/bin/env python3

from level_object import level
from cursor import cursor
from anim_sprite import animd_sprite
from static_sprite import static_sprite

class level_1(level):
    def put_inventroy_cursor(self):
        y = 305
        position = []
        size = []
        while y < 817:
            x = 418
            while x < 1386:
                position.append([x, y])
                size.append([123, 125])
                x += 121
            y += 128
        self.invent_cursor = cursor(size, position, (135, 206, 250), 5)
        self.invent_cursor.set_col_raw(8, 4)

    def __init__(self, surface, level):
        super().__init__(surface, level)
        self.dis_bg = animd_sprite('ressources/lvl1/diss', [0,0], 0.04, 19, 0)
        self.invent = static_sprite('ressources/invent.png', [250, 150])
        self.invent.set_size([1300, 800])
        self.dis_bg.set_size([1900, 1000])
        self.put_inventroy_cursor()