#!/usr/bin/env python3

import pygame as py
from level_object import level, animd_sprite, static_sprite, level_body
from lvl1_keys import LVL, LVL_scale, group, LVL_group, static
from text_and_button import text, button
from my_classic_func import *

class game_seeds():
    def init_img_and_history(self, background):
        self.bg = animd_sprite(background, [0, 0], 0.07, 119, 0)
        self.bg.set_size((1900, 1000))
        self.content = level_body("./src/.save.dange")
        self.sound = py.mixer.Sound('./lvl1/lvl1.ogg')
        self.history = get_file("./src/.history.dange")
        self.leader = get_file(".leader.dange")

    def init_text(self):
        bg = static_sprite("history.png", [0, 0])
        bg.set_size((1900, 1000))
        self.txt = text('med2.ttf', '', (255,255,255), 30)
        self.buttons = []
        self.param = []
        self.param2 = []
        self.back = []
        self.prev = ['menu']

    def __init__(self, background, window, surface):
        self.init_img_and_history(background)
        self.init_text()
#        self.butsound_mv = py.mixer.Sound('busound.ogg')
        self.window = window
        self.screen = surface
        self.fps = py.time.Clock()

    def new_button(self, img, pos, size, container):
        tmp = button(img, pos, size)
        container.append(tmp)

    def menu_bar_move_up(self, event):
        if event.key == py.K_DOWN and self.status == 'menu':
            tmp = self.buttons[self.index]
 #           self.butsound_mv.play()
            self.index += 1
            if self.index > 3:
                self.index = 0
            tmp2 = self.buttons[self.index]
            tmp.update((200, 100))
            tmp2.update((250, 120))

    def menu_bar_move_down(self, event):
        if event.key == py.K_UP and self.status == 'menu':
            tmp = self.buttons[self.index]
#            self.butsound_mv.play()
            self.index -= 1
            if self.index < 0:
                self.index = 3
            tmp2 = self.buttons[self.index]
            tmp.update((200, 100))
            tmp2.update((250, 120))

    def init_info(self):
        self.status = "info"
        self.current = -1
        self.txt.text = ''
        self.offset = 0
        self.speed = 0.1

    def manage_state(self, event):
        if event.key == py.K_RETURN and self.index == 0:
            self.status = 'Game'
        if event.key == py.K_ESCAPE and self.status != 'menu':
            self.status = 'menu'
        if event.key == py.K_RETURN and self.index == 3:
            self.window = False
        if event.key == py.K_RETURN and self.index == 2:
            self.init_info()
        if event.key == py.K_SPACE and self.status == "info":
            self.speed = 0.8
        if event.key == py.K_BACKSPACE and self.status == "info":
            self.speed = 0.1
        if event.key == py.K_DOWN and self.status == "tuto":
            if self.y > -1200:
                self.y -= 40
        if event.key == py.K_UP and self.status == "tuto":
            if self.y < 0:
                self.y += 40

    def manage_menu_param(self, event):
        if self.status == 'menu':
            if self.param[0].is_clicked(event.pos):
                self.prev.append(self.status)
                self.status = "leader"
#                self.butsound_mv.play()
            if self.param[1].is_clicked(event.pos):
                self.prev.append(self.status)
#                self.butsound_mv.play()
                self.status = "param"
            if self.param[2].is_clicked(event.pos):
                self.prev.append(self.status)
#                self.butsound_mv.play()
                self.status = "tuto"


    def manage_param_page(self, event):
        if self.status == "param":
            if self.param2[0].is_clicked(event.pos):
                self.game.sound.set_volume(0.5)
               # self.butsound_mv.play()
            if self.param2[1].is_clicked(event.pos):
                #self.butsound_mv.play()
                self.game.sound.set_volume(0)
            if self.param2[6].is_clicked(event.pos) and self.vol < 0.99:
                self.vol += 0.1
                #self.butsound_mv.play()
                self.game.sound.set_volume(self.vol)
            if self.param2[7].is_clicked(event.pos) and self.vol > 0:
                #self.butsound_mv.play()
                self.vol -= 0.1
                self.game.sound.set_volume(self.vol)
            if self.param2[8].is_clicked(event.pos) and self.fps_vlu < 120:
                self.fps_vlu += 10
               # self.butsound_mv.play()
            if self.param2[9].is_clicked(event.pos) and self.fps_vlu > 10:
               # self.butsound_mv.play()
                self.fps_vlu -= 10
        if self.status != 'menu':
            if self.back[0].is_clicked(event.pos):
                self.status = self.prev[-1]
                #self.butsound_mv.play()
                self.prev.pop(len(self.prev) - 1)

    def win_event(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.window = False

            if event.type == py.KEYDOWN:
                self.menu_bar_move_down(event)
                self.menu_bar_move_up(event)
                self.manage_state(event)

            if event.type == py.MOUSEBUTTONDOWN:
                self.manage_menu_param(event)
                self.manage_param_page(event)

    def draw_buttons(self, container):
        for elem in container:
            self.screen.blit(elem.img, elem.rect)

    def draw_on_rect(self, word, color1, color2, size, lenght, first, offset):
        x, y = first
        for elem in word:
            tmp = elem.split(';', 1)
            py.draw.rect(self.screen, color1, ((x, y), size), lenght)
            txt = text('med2.ttf', tmp[1], color2, 30)
            txt.draw(self.screen, [x,y])
            y += offset