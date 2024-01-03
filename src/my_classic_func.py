#!/usr/bin/env python3

import pygame as py

def get_file(file):
    tmp = ''
    with open(file, "r") as map:
        tmp = map.read()
    return tmp

def get_the_elem(map, elem):
    for line in map:
        key = line.split(':', 1)
        if key[0] == elem:
            return key[1]

def diff_time(milli_sec):
    t1 = py.time.get_ticks()
    t2 = py.time.get_ticks()
    if (t2 - t1) > milli_sec:
         return True
    else:
         return False

def is_empty(group):
    if group.__len__() == 0:
            return True
    return False

def move_rect(rect, where, offset):
        x,y = rect
        if where == "R":
            x = x - offset
        if where == "L":
            x = x + offset
        if where == "U":
            y = y + offset
        if where == "D":
            y = y - offset
        return [x,y]