#!/usr/bin/env python3

import pygame as py

from game_seeds import *
from level1 import level_1

class final_game_obj(game_seeds):
    def __init__(self, background, window, surface, cursor):
        super().__init__(background, window, surface, cursor)
        self.level_1 = level_1(self.screen, "lvl1")
        self.level_1.set_cursor(cursor)
        self.level_1.init_map()
        self.status = 'logo'
        self.index = 0
        self.timer = 0

    def init_button(self):
        self.side = []
        self.choose = []
        self.users_button = listing_buttons(['users'])
        add = py.image.load('ressources/menu//button/mini/add.png')
        retire = py.image.load('ressources/menu//button/mini/retire.png')
        back_and_left = py.image.load('ressources/menu//button/mini/back.png')
        self.buttons.new_button(py.image.load('ressources/menu/button/start.png'), [250, 200], (200, 100))
        self.buttons.new_button(py.image.load('ressources/menu//button/play.png'), [250, 350], (200, 100))
        self.buttons.new_button(py.image.load('ressources/menu//button/info.png'), [250, 500], (200, 100))
        self.buttons.new_button(py.image.load('ressources/menu//button/quit.png'), [250, 650], (200, 100))
        self.new_button(py.image.load('ressources/menu//button/mini/leader.png'), [1700, 0], (50, 50), self.param)
        self.new_button(py.image.load('ressources/menu//button/mini/param.png'), [1770, 0], (50, 50), self.param)
        self.new_button(py.image.load('ressources/menu//button/mini/tuto.png'), [1840, 0], (50, 50), self.param)
        self.new_button(py.image.load('ressources/menu//button/mini/sound+.png'), [100, 0], (100, 100), self.param2)
        self.new_button(py.image.load('ressources/menu//button/mini/sound-.png'), [300, 0], (100, 100), self.param2)
        self.new_button(py.image.load('ressources/menu//button/mini/save+.png'), [100, 200], (100, 100), self.param2)
        self.new_button(py.image.load('ressources/menu//button/mini/save-.png'), [300, 200], (100, 100), self.param2)
        self.new_button(py.image.load('ressources/menu//button/mini/achv.png'), [100, 400], (100, 100), self.param2)
        self.new_button(py.image.load('ressources/menu//button/mini/buy.png'), [300, 400], (100, 100), self.param2)
        self.new_button(add, [100, 600], (100, 100), self.param2)
        self.new_button(retire, [700, 600], (100, 100), self.param2)
        self.new_button(add, [100, 800], (100, 100), self.param2)
        self.new_button(retire, [700, 800], (100, 100), self.param2)
        self.new_button(back_and_left, [1600, 0], (50, 50), self.back)
        self.new_button(back_and_left, [450, 450], (80, 80), self.side)

    def init_choose_button(self):
        self.index2 = 0
        self.new_button(py.image.load('./ressources/menu/choose/Bigtree.png'), [650, 150], (600, 600), self.choose)
        self.new_button(py.image.load('./ressources/menu/choose/Snow.png'), [650, 150], (600, 600), self.choose)
        self.new_button(py.image.load('./ressources/menu/choose/Oasis.png'), [650, 150], (600, 600), self.choose)
        self.new_button(py.image.load('./ressources/menu/choose/Town.png'), [650, 150], (600, 600), self.choose)
        self.new_button(py.image.load('./ressources/menu/button/mini/left.png'), [1350, 450], (80, 80), self.side)
        self.new_button(py.image.load('./ressources/menu/button/mini/resume.png'), [1050, 800], (60, 60), self.side)

    def init_users_button(self):
        self.cursor.execute("""SELECT guild_name FROM guilds""")
        self.users = self.cursor.fetchall()
        user_image = py.image.load('./ressources/menu/button/user.png')
        y = 100
        for i in self.users:
            self.users_button.new_button(user_image, [250, y], (370, 120))
            y += 150
        if len(self.users_button.menu) != 0:
            self.users_button.menu[0].update((420,140))

    def last_loading(self):
        tmp = self.buttons.menu[self.index]
        tmp.update((250, 120))
        self.cursor.execute("""SELECT * FROM guilds ORDER BY best_scr DESC LIMIT 7""")
        self.data = self.cursor.fetchall()
        tuto = get_file(".tuto.dange")
        self.tuto = text('font/med2.ttf', tuto, (0,0,0), 30)
        self.x, self.y = [0, 0]
        self.vol = 0.5
        self.fps_vlu = 120

    def menu_state(self):
        self.screen.blit(self.bg.image, self.bg.rect)
        self.bg.play(0)
        self.buttons.draw(self.status, self.screen)
        self.draw_buttons(self.param)

    def users_state(self):
        self.screen.blit(self.bg.image, self.bg.rect)
        self.bg.play(0)
        self.users_button.draw(self.status, self.screen)
        self.draw_buttons(self.back)
        y = 120
        txt2 = text('font/med2.ttf', "Choose player account", (0,0,0), 40)
        txt2.draw(self.screen, [30, 10])
        for i in self.users:
            txt = text('font/med2.ttf', i[0], (0,0,0), 40)
            txt.draw(self.screen, [300, y])
            y += 150

    def article_state(self):
        self.screen.blit(self.buy_bg.image, self.buy_bg.rect)
        self.buy_bg.play(0)
        j = self.locate
        self.draw_buttons(self.back)
        txt = text('font/med2.ttf', self.article, (255,255,255), 30)
        y = self.article.count('\n')*40 + 280
        txt2 = text('font/med2.ttf', self.buy_images[j].txt, (0,0,0), 30)
        var1 = self.buy_images[j].img.get_rect()
        var2 = self.buy_button[j].img.get_rect()
        var1.topleft = [110, 90]
        var2.topleft = [10, 0]
        txt.draw(self.screen, [0, 220])
        self.screen.blit(self.buy_images[j].img, var1)
        self.screen.blit(self.buy_button[j].img, var2)
        py.draw.rect(self.screen, (255,255,255), ((430, y+10), (110, 50)), 0)
        txt2.draw(self.screen, [430, y+10])
        self.screen.blit(self.buy_image, [260, y])
        self.screen.blit(py.transform.scale(self.money_img, [30,30]), (510, y+15))

    def param_state(self):
        self.screen.blit(self.bg.image, self.bg.rect)
        self.bg.play(0)
        self.draw_buttons(self.param2)
        self.draw_buttons(self.back)
        if self.vol < 0:
            self.vol = 0
        py.draw.rect(self.screen, (0,0,0), ((200, 620), (480, 50)), 0)
        txt = text('font/med2.ttf', f'Musique: {int((self.vol*100) / 2)}%', (255,255,255), 30)
        txt.draw(self.screen, [200, 620])
        py.draw.rect(self.screen, (0,0,0), ((200, 820), (480, 50)), 0)
        txt = text('font/med2.ttf', f'FPS:{self.fps_vlu} per second', (255,255,255), 30)
        txt.draw(self.screen, [200, 820])

    def tuto_state(self):
        self.screen.blit(self.bg.image, self.bg.rect)
        self.bg.play(0)
        self.draw_buttons(self.back)
        tuto_pos = [self.x, self.y]
        self.tuto.draw(self.screen, tuto_pos)

    def info_state(self):
        self.screen.blit(self.bg_info.image, self.bg_info.rect)
        self.txt.draw(self.screen, [0, 0])
        self.draw_buttons(self.back)
        if (int(self.offset) > self.current):
            self.current = int(self.offset)
            self.txt.text += self.history[self.current]
        if (int(self.offset) < len(self.history)-1):
            self.offset += self.speed

    def leader_state(self):
        self.screen.blit(self.bg.image, self.bg.rect)
        self.bg.play(0)
        self.draw_buttons(self.back)
        self.draw_on_rect(self.data, (0,0,0), (255,255,255), (400, 50), 0, (500, 150), 70)

    def play_state(self):
        self.screen.blit(self.bg.image, self.bg.rect)
        self.bg.play(0)
        self.draw_buttons(self.back)        
        py.draw.rect(self.screen, (255,255,255), ((200, 220), (500, 70)), 0)
        py.draw.rect(self.screen, (0,0,0), ((200, 220), (500, 70)), 2)
        txt = text('font/med2.ttf', self.user, (0,0,0), 30)
        txt2 = text('font/med2.ttf', 'Please enter the username (Only alphanumeric character):', (255,255,255), 30)
        txt.draw(self.screen, [200, 220])
        txt2.draw(self.screen, [200, 120])

    def buy_state(self):
        self.screen.blit(self.buy_bg.image, self.buy_bg.rect)
        self.buy_bg.play(0)
        self.draw_buttons(self.back)
        self.draw_buttons(self.buy_button)
        x, y = 40, 15
        for i in self.buy_images:
            self.screen.blit(i.img, i.rect)
            py.draw.rect(self.screen, (255,255,255), ((x, y+130), (70, 30)), 0)
            txt = text('font/med2.ttf', i.txt, (0,0,0), 20)
            txt.draw(self.screen, [x, y+130])
            x += 250
            if x > 1500:
                x = 40
                y += 200

    def choose_state(self):
        self.screen.blit(self.bg.image, self.bg.rect)
        self.bg.play(0)
        self.draw_buttons(self.side)
        self.draw_buttons(self.back)        
        arc = ['FantasticVerdant Enigma', 'Frozen Ascent', 'Oasis of Lost Magic', 'Epic showdown']
        part = ['2 part', '1 part', '2 part', '1 part']
        txt = text('font/med2.ttf', arc[self.index2], (0,0,0), 30)
        txt2 = text('font/med2.ttf', f"Number of arc: {part[self.index2]}", (255,255,255), 30)
        txt.draw(self.screen, [750, 100])
        tmp = self.choose[self.index2]
        self.screen.blit(tmp.img, tmp.rect)
        py.draw.rect(self.screen, (255,255,255), tmp.rect, 8)
        py.draw.rect(self.screen, (0,0,0), ((700, 800), (300, 60)), 0)
        txt2.draw(self.screen, [700, 800])

    def logo_state(self):
        self.screen.blit(self.logo_bg.image, self.logo_bg.rect)
        self.logo_bg.play(0)
        speed, off = self.logo_bg.inc_speed, self.logo_bg.offset
        self.timer += speed + off
        if self.timer > (self.logo_bg.max + 5 + off):
            self.status = 'menu'
            self.sound.play(-1)

    def start_state(self):
        self.level_1.run()
        self.draw_buttons(self.param)
        txt = text('font/med2.ttf', str(self.user_data[3]), (255,255,255), 20)
        py.draw.rect(self.screen, (155,0,0), ((1500, 10), (100, 30)), 0)
        txt.draw(self.screen, [1500, 10])
        self.screen.blit(self.money_img, (1580, 10))

    def game_state(self):
        self.sound.stop()
        self.level_1.snd_game.play(-1)
        self.cursor.execute("""SELECT * FROM guilds WHERE guild_name = ?""", (self.user,))
        self.user_data = self.cursor.fetchall()[0]
        self.status = 'start'

    def state_manager(self):
        if (self.status == 'logo'):
            self.logo_state()
        elif (self.status == 'menu'):
            self.menu_state()
        elif self.status == 'choose':
            self.choose_state()
        elif (self.status == 'Game'):
            self.game_state()
        elif (self.status == 'start'):
            self.start_state()
        elif (self.status == 'param'):
            self.param_state()
        elif (self.status == 'tuto'):
            self.tuto_state()
        elif (self.status == 'users'):
            self.users_state()
        elif (self.status == 'leader'):
            self.leader_state()
        elif self.status == 'info':
            self.info_state()
        elif self.status == 'play':
            self.play_state()
        elif self.status == 'buy':
            self.buy_state()
        elif self.status == 'article':
            self.article_state()

    def init_rect_info(self):
        self.buy_button = []
        self.buy_images = []
        cadre = ['./ressources/market/cadre/bronze.png', './ressources/market/cadre/argent.png',
                './ressources/market/cadre/or.png']
        x, y, z = 40, 15, 0
        for i in self.market:
            self.new_button(py.image.load(cadre[i[9]]), [x-80, y-70], (250, 250), self.buy_button)
            self.new_button(py.image.load(i[1]), [x+25, y+20], (60, 60), self.buy_images)
            tmp = self.buy_button[z]
            tmp.set_des(i[10])
            tmp2 = self.buy_images[z]
            tmp2.set_des(str(i[2]))
            z += 1
            x += 250
            if x > 1500:
                x = 40
                y += 200
        self.buy_bg.set_size((1900, 1000))

    def run(self):
        self.init_button()
        self.last_loading()
        self.bg_info = static_sprite('ressources/ko.jpg', [0, 0])
        self.cursor.execute("""SELECT * FROM market ORDER BY price""")
        self.market = self.cursor.fetchall()
        self.init_rect_info()
        self.init_choose_button()
        self.init_users_button()
        self.money_img = py.image.load('ressources/dange.jpg')
        self.buy_image = py.image.load('ressources/menu/button/buy.png')
        self.money_img = py.transform.scale(self.money_img, [20, 20])
        self.buy_image = py.transform.scale(self.buy_image, [150, 75])
        self.init_or_not = False
        while self.window:
            self.screen.fill((0,0,0))
            self.state_manager()
            if not self.init_or_not and self.level_1.status in ['arena_me', 'arena_select', 'arena_select2']:
                self.init_user_data()
                self.init_or_not = True
            if self.level_1.status == 'ext':
                self.init_or_not = False
            self.fps.tick(600)
            py.display.flip()
            self.win_event()