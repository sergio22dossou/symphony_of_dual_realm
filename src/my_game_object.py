#!/usr/bin/env python3

import pygame as py

from game_seeds import *

class final_game_obj(game_seeds):
    def __init__(self, background, window, surface):
        super().__init__(background, window, surface)

    def init_button(self):
        self.game = level(True, self.screen, "lvl1", LVL, LVL_scale, group, LVL_group, static)
        self.game.init_map()
        self.level = get_the_elem(self.content.map, "level")
        self.status = 'menu'
        self.index = 0
        self.new_button('./button/start.png', [250, 200], (200, 100), self.buttons)
        self.new_button('./button/play.png', [250, 350], (200, 100), self.buttons)
        self.new_button('./button/info.png', [250, 500], (200, 100), self.buttons)
        self.new_button('./button/quit.png', [250, 650], (200, 100), self.buttons)
        self.new_button('./button/mini/leader.png', [1700, 0], (50, 50), self.param)
        self.new_button('./button/mini/param.png', [1770, 0], (50, 50), self.param)
        self.new_button('./button/mini/tuto.png', [1840, 0], (50, 50), self.param)
        self.new_button('./button/mini/sound+.png', [100, 0], (100, 100), self.param2)
        self.new_button('./button/mini/sound-.png', [300, 0], (100, 100), self.param2)
        self.new_button('./button/mini/save+.png', [100, 200], (100, 100), self.param2)
        self.new_button('./button/mini/save-.png', [300, 200], (100, 100), self.param2)
        self.new_button('./button/mini/achv.png', [100, 400], (100, 100), self.param2)
        self.new_button('./button/mini/buy.png', [300, 400], (100, 100), self.param2)
        self.new_button('./button/mini/add.png', [100, 600], (100, 100), self.param2)
        self.new_button('./button/mini/retire.png', [700, 600], (100, 100), self.param2)
        self.new_button('./button/mini/add.png', [100, 800], (100, 100), self.param2)
        self.new_button('./button/mini/retire.png', [700, 800], (100, 100), self.param2)
        self.new_button('./button/mini/back.png', [1600, 0], (50, 50), self.back)

    def last_loading(self):
        tmp = self.buttons[self.index]
        tmp.update((250, 120))
        self.data = self.leader.split('\n', self.leader.count('\n'))
        tuto = get_file(".tuto.dange")
        self.tuto = text('med2.ttf', tuto, (0,0,0), 30)
        self.x, self.y = [0, 0]
        self.vol = 0.5
        self.fps_vlu = 120

    def menu_state(self):
        self.screen.blit(self.bg.image, self.bg.rect)
        self.bg.update(0)
        self.draw_buttons(self.buttons)
        self.draw_buttons(self.param)

    def param_state(self):
        self.screen.blit(self.bg.image, self.bg.rect)
        self.bg.update(0)
        self.draw_buttons(self.param2)
        self.draw_buttons(self.back)
        py.draw.rect(self.screen, (0,0,0), ((200, 620), (480, 50)), 0)
        txt = text('med2.ttf', f'Musique: {int(self.vol*100)}%', (255,255,255), 30)
        txt.draw(self.screen, [200, 620])
        py.draw.rect(self.screen, (0,0,0), ((200, 820), (480, 50)), 0)
        txt = text('med2.ttf', f'FPS:{self.fps_vlu} per second', (255,255,255), 30)
        txt.draw(self.screen, [200, 820])

    def tuto_state(self):
        self.screen.blit(self.bg.image, self.bg.rect)
        self.bg.update(0)
        self.draw_buttons(self.back)
        tuto_pos = [self.x, self.y]
        self.tuto.draw(self.screen, tuto_pos)

    def info_state(self):
        self.screen.blit(self.bg_info.image, self.bg_info.rect)
        self.txt.draw(self.screen, [0, 0])
        if (int(self.offset) > self.current):
            self.current = int(self.offset)
            self.txt.text += self.history[self.current]
        if (int(self.offset) < len(self.history)-1):
            self.offset += self.speed

    def leader_state(self):
        self.screen.blit(self.bg.image, self.bg.rect)
        self.bg.update(0)
        self.draw_buttons(self.back)
        self.data.sort(reverse=True)
        self.draw_on_rect(self.data, (0,0,0), (255,255,255), (400, 50), 0, (500, 150), 70)

    def state_manager(self):
        if (self.status == 'menu'):
            self.menu_state()
        elif (self.status == 'Game'):
             self.game.run()
        elif (self.status == 'param'):
            self.param_state()
        elif (self.status == 'tuto'):
            self.tuto_state()
        elif (self.status == 'leader'):
            self.leader_state()
        elif self.status == 'info':
            self.info_state()

    def run(self):
        self.init_button()
        self.last_loading()
        self.bg_info = static_sprite('ko.jpg', [0, 0])
        while self.window:
            self.screen.fill((0,0,0))
            self.state_manager()
            self.fps.tick(600)
            py.display.flip()
            self.win_event()