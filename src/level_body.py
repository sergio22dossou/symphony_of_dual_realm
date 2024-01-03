import pygame as py

class level_body: #this represent the design of the level create from a file
    def __init__(self, file_name):
        stri = ''
        if len(file_name) == 0:
            return 0
        with open(file_name, "r") as map:
            stri = map.read()
        self.map = stri.split('\n', stri.count('\n'))