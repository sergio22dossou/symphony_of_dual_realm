#!/usr/bin/env python3

import pygame as py
from level_object import level, animd_sprite, static_sprite, level_body
from text_and_button import text, button, listing_buttons
from my_classic_func import *

def is_caps_word(event):
    if (event.mod & py.KMOD_SHIFT) or (event.mod & py.KMOD_CAPS):
        return py.key.name(event.key).upper()
    else:
        return py.key.name(event.key)

class game_seeds():
    def init_img_and_history(self, background):
        self.bg = animd_sprite(background, [0, 0], 0.05, 119, 0)
        self.buy_bg = animd_sprite("ressources/market_bg", [0, 0], 0.05, 6, 0)
        self.logo_bg = animd_sprite("ressources/logo", [600, 300], 0.02, 50, 0)
        self.bg.set_size((1900, 1000))
        self.index_usr = 0
        self.content = level_body("./src/.save.dange")
        self.sound = py.mixer.Sound('ressources/menu/game.ogg')
        self.history = get_file("./src/.history.dange")

    def init_text(self):
        self.txt = text('font/med2.ttf', '', (255,255,255), 30)
        self.buttons = listing_buttons(['menu'])
        self.param = []
        self.param2 = []
        self.back = []
        self.prev = ['menu']

    def init_user_data(self):
        self.cursor.execute("""SELECT id_guild FROM guilds WHERE guild_name = ?""", (self.user,))
        tmp = self.cursor.fetchall()[0]
        self.dt_guild = tmp
        self.cursor.execute("""SELECT * FROM players WHERE id_guild = ?""", (tmp[0],))
        self.team = self.cursor.fetchall()
        print("ice: ", end='')
        print(self.team)
        self.level_1.set_data(self.team)

    def __init__(self, background, window, surface, cursor):
        self.init_img_and_history(background)
        self.init_text()
        self.cursor = cursor
        self.window = window
        self.screen = surface
        self.fps = py.time.Clock()

    def new_button(self, img, pos, size, container):
        tmp = button(img, pos, size)
        container.append(tmp)

    def init_info(self):
        self.status = "info"
        self.current = -1
        self.txt.text = ''
        self.offset = 0
        self.speed = 0.1

    def manage_state_1(self, event):
        if event.key == py.K_RETURN and self.status == 'choose':
            self.init_user_data()
            self.status = 'Game'
        if event.key == py.K_RETURN and self.status == 'users':
            self.user = self.users[self.index][0]
            self.prev.append(self.status)
            self.status = 'choose'

    def manage_menu_buttons(self):
        if self.buttons.index == 0:
            self.prev.append(self.status)
            self.index = 0
            self.status = 'users'
        if self.buttons.index == 1:
            self.prev.append(self.status)
            self.status = 'play'
            self.user = ''
        if self.buttons.index == 2:
            self.prev.append(self.status)
            self.init_info()
        if self.buttons.index == 3:
            self.window = False

    def manage_state_2(self, event):
        if event.key == py.K_RETURN and self.status == 'play':
            self.cursor.execute("""INSERT INTO guilds (guild_name, level, money, best_scr, best_niv) VALUES (?, 0, 1000, 0, 0)""", (self.user,))
            self.cursor.execute("""SELECT id_guild FROM guilds WHERE guild_name = ?""", (self.user,))
            vlue = self.cursor.fetchall()[0][0]
            self.cursor.execute("""INSERT INTO players (id_guild, path, perso, type, vit, life, res, mana, xp, desc) VALUES (?, "./ressources/players/lucas.png", "Lucas", "c", 30, 60, 15, 100, 0, "Marques, a half-man, half-god demigod, walks the realms with unparalleled determination. As a devoted servant of Azaka Medeh, the benevolent god of agriculture, Marques tends to the earth with his powerful hands. His roots in both the divine and earthly realms make him a force to be reckoned with. In the face of a mysterious virus threatening both worlds, Marques embarks on a daring journey, uncovering secrets and facing astonishing beings to break the curse that plagues the kingdom")""", (vlue,))
            self.init_user_data()
            self.status = 'Game'
        if event.key == py.K_RETURN and self.status == 'menu':
            self.manage_menu_buttons()
        if event.key == py.K_SPACE and self.status == "info":
            self.speed = 0.8
        if event.key == py.K_BACKSPACE and self.status == "info":
            self.speed = 0.1

    def manage_menu_state(self, event):
        self.manage_state_1(event)
        self.manage_state_2(event)

    def manage_param_state(self, event):
        if event.key == py.K_DOWN and self.status == "tuto":
            if self.y > -1400:
                self.y -= 40
        if event.key == py.K_UP and self.status == "tuto":
            if self.y < 0:
                self.y += 40

    def manage_play_state(self, event):
        if event.key == py.K_BACKSPACE:
            self.user = self.user[:-1]
        elif (event.key >= 97 and event.key <= 127) or (event.key >= 48 and event.key <= 57):
            self.user += is_caps_word(event)

    def manage_state(self, event):
        if self.status == 'play': self.manage_play_state(event)
        self.manage_menu_state(event)
        self.manage_param_state(event)

    def manage_menu_param(self, event):
        if self.status in ['menu', 'start']:
            if self.param[0].is_clicked(event.pos):
                self.prev.append(self.status)
                self.status = "leader"
            if self.param[1].is_clicked(event.pos):
                self.prev.append(self.status)
                self.status = "param"
            if self.param[2].is_clicked(event.pos):
                self.prev.append(self.status)
                self.x, self.y = 0, 0
                self.status = "tuto"

    def manage_volume(self, event):
        if self.param2[0].is_clicked(event.pos):
            self.sound.set_volume(0.5)
        if self.param2[1].is_clicked(event.pos):
            self.sound.set_volume(0)
        if self.param2[6].is_clicked(event.pos) and self.vol < 1.99:
            self.vol += 0.1
            self.sound.set_volume(self.vol)
        if self.param2[7].is_clicked(event.pos) and self.vol >= 0:
            self.vol -= 0.1
            self.sound.set_volume(self.vol)

    def manage_buy_and_fps(self, event):
        if self.param2[5].is_clicked(event.pos):
            self.prev.append(self.status)
            self.status = 'buy'            
        if self.param2[8].is_clicked(event.pos) and self.fps_vlu < 120:
            self.fps_vlu += 10
        if self.param2[9].is_clicked(event.pos) and self.fps_vlu > 10:
            self.fps_vlu -= 10

    def manage_back_button(self, event):
        if self.status not in ['game', 'menu', 'start']:
            if self.back[0].is_clicked(event.pos):
                self.status = self.prev[-1]
                self.prev.pop(len(self.prev) - 1)
                self.users_button.restart_menu_bar((370, 120))
                self.user = ''

    def manage_param_page(self, event):
        if self.status == "param":
            self.manage_volume(event)
            self.manage_buy_and_fps(event)
        self.manage_back_button(event)

    def manage_choose_state(self, event):
        if self.status == 'choose':
            if event.key == py.K_LEFT:
                self.index2 -= 1
            elif event.key == py.K_RIGHT:
                self.index2 += 1
        if self.index2 > 3:
            self.index2 = 0
        if self.index2 < 0:
            self.index2 = 3

    def manage_market_click(self, event):
        if self.status == 'buy':
            j = 0
            for i in self.buy_button:
                if i.is_clicked(event.pos):
                    self.prev.append(self.status)
                    self.status = "article"
                    self.article = i.txt
                    self.locate = j
                j += 1

    def manage_gameplay_event(self, level, event):
        if level.status == "arena_select2":
            level.move_the_select_cursor(event.key, level.select3)
            if event.key == py.K_ESCAPE:
                level.status = "arena_select"
            if event.key == py.K_RETURN:
                level.user_fight()
                level.load_sortilege_enem()
                level.status = "arena_enem"
        if level.status == 'arena_select':
            level.move_the_select_cursor(event.key, level.select2)
            if event.key == py.K_ESCAPE:
                level.status = "arena_me"
            if event.key == py.K_RETURN:
                level.status = "arena_select2"
        if level.status == 'arena_me':
            level.move_the_select_cursor(event.key, level.select)
            if event.key == py.K_RETURN:
                level.load_sortilege(level.select.index)
                level.status = "arena_select"

    def manage_choose_click(self, event):
        if self.status == 'choose':
            if self.side[0].is_clicked(event.pos):
                self.index2 -= 1
            if self.side[1].is_clicked(event.pos):
                self.index2 += 1
            if self.side[2].is_clicked(event.pos):
                self.status = 'Game'

    def win_event(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.window = False

            if event.type == py.KEYDOWN:
                self.buttons.bar_move_down(event, self.status)
                self.buttons.bar_move_up(event, self.status)
                self.users_button.bar_move_up(event, self.status)
                self.users_button.bar_move_down(event, self.status)
                self.manage_state(event)
                self.manage_choose_state(event)
                self.manage_gameplay_event(self.level_1, event)
                self.level_1.event_of_level(event)

            if event.type == py.MOUSEBUTTONDOWN:
                self.manage_menu_param(event)
                self.manage_param_page(event)
                self.manage_market_click(event)
                self.manage_choose_click(event)

    def draw_buttons(self, container):
        for elem in container:
            self.screen.blit(elem.img, elem.rect)

    def draw_on_rect(self, word, color1, color2, size, lenght, first, offset):
        x, y = first
        for elem in word:
            py.draw.rect(self.screen, color1, ((x, y), size), lenght)
            txt = text('font/med2.ttf', f'{elem[1]}: {elem[4]} (level {elem[2]})', color2, 30)
            txt.draw(self.screen, [x,y])
            y += offset