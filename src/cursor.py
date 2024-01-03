#!/usr/bin/env python3

import pygame as py

class cursor():
    def __init__(self, size, positions, color, thick):
        self.index = 0
        self.positions = positions
        self.color = color
        self.size = size
        self.thick = thick
        self.col = len(self.positions)
        self.raw = 1

    def set_col_raw(self, col, raw):
        self.col = col
        self.raw = raw

    def draw(self, screen):
        pos = self.positions[self.index]
        size = self.size[self.index]
        py.draw.rect(screen, self.color, (pos, size), self.thick)

    def move_hori(self, move):
        max = self.col*self.raw
        if not any(self.positions) or not any(self.size):
            return 0
        if move:
            self.index += 1
        else:
            self.index -= 1
        if self.index > max-1:
            self.index = 0
        elif self.index < 0:
            self.index = max - 1

    def move_verti(self, move):
        max = self.col*self.raw
        if not any(self.positions) or not any(self.size):
            return 0
        if move:
            self.index += self.col
        else:
            self.index -= self.col
        if self.index > max-1:
            self.index = self.index % max
        elif self.index < 0:
            self.index = self.index % max
