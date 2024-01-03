#!/usr/bin/env python3

import pygame as py
from text_and_button import *
from my_classic_func import *
from level_body import *
from level_class_steps import *

class level(level_manager):
    def __init__(self, surface, level):
        super().__init__(surface, level)
        self.is_play = False
        self.diss_start = True

    def event_of_level(self, event):
        test = self.status.split('_', 1)
        if self.status == "diss":
            self.event_diss(event.key)
        if self.status == "invent":
            self.event_invent(event.key)
        if event.key == py.K_SPACE and self.status != "diss":
            self.status = "invent"
        if event.key == py.K_ESCAPE and test != "arena":
            self.status = "ext"
        if event.key == py.K_RETURN and self.is_contact and \
           self.status == 'ext':
            self.status = "dis"
        if event.key == py.K_RETURN and self.new_contact and \
           self.status == 'ext':
            self.set_the_portal()

    def run(self):
        self.surface.fill((0, 0, 0))
        if self.status == 'invent':
            self.surface.fill((204,182,135))
            self.surface.blit(self.invent.image, self.invent.rect)
            self.invent_cursor.draw(self.surface)
        if self.status == "ext":
            self.manage_ext_state()
        if self.status == "dis":
            self.load_diss()
        if self.status == "diss":
            self.manage_dis()
        if self.status == "enemy":
            self.init_enemy()
            self.load_sortilege_enem()
            self.status = "arena_me"
        test = self.status.split('_', 1)
        if test[0] == "arena":
            self.manage_arena_state()