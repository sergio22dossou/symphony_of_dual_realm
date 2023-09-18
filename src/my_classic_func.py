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