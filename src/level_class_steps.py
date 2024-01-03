import pygame as py
from level_body import *
from anim_sprite import *
from static_sprite import *
import random
import json
from cursor import cursor
from character import badguy, player
from my_classic_func import *
from text_and_button import text

class level_init:
    def first_data_json(self, level):
        with open('./level_data/'+level+'.json', 'r') as json_file:
            file = json.load(json_file)
            self.key = file.get("LVL", {})
            self.status = "ext"
            self.scale = file.get("LVL_scale", {})
            self.level = level_body(file.get("LVL_body", ""))
            self.key_grp = file.get("LVL_group", {})
            prlx = file.get("paralax", "")
            self.static = file.get("static", [])
            self.animated = file.get("animated", {})
            self.animd_keys = file.get("animd_keys", [])
            self.png_info = file.get("png_script", [])
            self.portal_info = file.get("portal", [])
        if len(prlx):
            self.prlx = py.image.load(prlx)
        else:
            self.prlx = 0

    def first_data_no_json(self, level):
        if self.prlx:
            self.prlx_rect = self.prlx.get_rect()
        self.fg_bg = static_sprite('./ressources/'+level+'/fg_bg.png', [0,0])
        self.fg_grd = static_sprite('./ressources/'+level+'/fg_grd.png', [0,0])
        self.snd_game = py.mixer.Sound("./ressources/"+level+"/ziq.ogg")
        self.snd_fg = py.mixer.Sound("./ressources/"+level+"/fg.ogg")
        self.fg_bg.image = py.transform.scale(self.fg_bg.image, [1900,1000])
        self.fg_grd.image = py.transform.scale(self.fg_grd.image, [1900,1000])
        self.state = 0

    def __init__(self, surface, level):
        self.surface = surface
        self.first_data_json(level)
        self.first_data_no_json(level)

    def set_cursor(self, cursor):
        self.cursor = cursor

    def loading_img(self):
        self.img_keys = {}
        for elem in self.static:
            spr = py.image.load(self.key[elem])
            self.img_keys[elem] = spr

    def init_group(self):
        self.dec = [0,0]
        self.path = py.sprite.Group()
        self.decor = py.sprite.Group()
        self.new_map = py.sprite.Group()
        self.animd = py.sprite.Group()
        self.png = py.sprite.Group()
        self.anex = py.sprite.Group()
        self.lucas = animd_sprite("ressources/lvl1/Lucas", [250, 300], 0.05, 2, 0)
        self.lucas.set_size = (10, 10)
        self.is_contact = False

    def init_paralax_img(self):
        i, j = 0, 0
        while j < 1000:
            while i < 1900:
                spr = static_sprite(self.prlx, [i, j])
                self.anex.add(spr)
                i += self.prlx_rect.size[0]
            j += self.prlx_rect.size[1]

    def init_map(self):
        self.init_group()
        x, y = 0, 0
        self.loading_img()
        self.arena = []
        #self.init_paralax_img()
        for line in self.level.map:
            x = 0
            for elem in line:
                spr = static_sprite(self.key[' '], [x, y])
                spr.image = py.transform.scale(spr.image, (70,70))
                self.path.add(spr)
                if elem == '!':
                    self.arena.append([x,y])
                if elem in self.static and elem != ' ':
                    spr = loaded_sprite(self.img_keys[elem], [x, y])
                    spr.image = py.transform.scale(spr.image, self.scale[elem])
                    spr.rect.size = self.scale[elem]
                    tmp = getattr(self, self.key_grp[elem])
                    tmp.add(spr)
                elif elem in self.animated:
                    i = self.animd_keys[elem]
                    spr = animd_sprite(self.key[elem], [x, y], i[0], i[1], i[2])
                    spr.set_size(self.scale[elem])
                    tmp = getattr(self, self.key_grp[elem])
                    tmp.add(spr)
                x += 50
            y += 50

    def init_enemy(self):
        num = random.randint(1, 3)
        x, y = 200, 300
        positions, size = [], []
        for i in range(0, num):
            level = random.randint(1, 2)
            self.cursor.execute("""SELECT * FROM monsters WHERE grade = ?""", (level,))
            tmp = self.cursor.fetchall()
            elem = tmp[random.randint(0,len(tmp)-1)]
            self.data_e.append(elem)
            spr = badguy(elem[1], [x, y], elem[-2], elem[-1], 0, elem)
            self.fg_enem.add(spr)
            positions.append([x, y])
            size.append(spr.rect.size)
            y += 250
        self.select3 = cursor(size, positions, (240,204,40), 3)

    def init_fight(self):
        self.status = "enemy"
        x, y = 1200, 350
        positions, size = [], []
        for elem in self.data:
            positions.append([x, y])
            size.append((100, 100))
            y += 50
        self.select = cursor(size, positions, (240,204,40), 3)
        self.data_e = []
        self.fg_enem = py.sprite.Group()
        self.snd_game.stop()
        self.snd_fg.play(-1)

class level_init_and_collision(level_init):
    def __init__(self, surface, level):
        super().__init__(surface, level)

    def is_inter(self, vlue, a, b):
        if (vlue >= a and vlue <= b):
            return True
        else:
            return False

    def is_png(self):
        num = 0
        for i in self.png:
            if i.rect.colliderect(self.lucas.rect): return num+1
            num += 1
        return False

    def is_portal(self):
        num = 0
        for i in self.new_map:
            if i.rect.colliderect(self.lucas.rect)\
                and self.detect(i.rect, self.lucas.rect, "D"):
                return num+1
            num += 1
        return False

    def detect(self, rec1, rec2, move):
        pos1, pos2 = rec1.topleft, rec2.topleft
        s1, s2 = rec1.size, rec2.size
        if (move == 'D' and pos1[1] < pos2[1] and pos1[0] < pos2[0]+s2[0]-9):
            return True
        if (move == 'U' and pos1[1] > pos2[1] and pos1[0] < pos2[0]+s2[0]-9):
            return True
        if (move == 'R' and pos1[0] < pos2[0]
            and (self.is_inter(pos1[1], pos2[1], pos2[1]+s2[1]-7) or
            self.is_inter(pos2[1], pos1[1], pos1[1]+s1[1]-7))):
            return True
        if (move == 'L' and pos1[0] > pos2[0] and
            ( self.is_inter(pos1[1], pos2[1], pos2[1]+s2[1]-7) or
            self.is_inter(pos2[1], pos1[1], pos1[1]+s1[1]-7))):
            return True
        return False

    def is_colliding(self, perso, grp, move):
        for elem in grp:
            if (perso.rect.colliderect(elem.rect) and 
                self.detect(perso.rect, elem.rect, move)):
                return True
        return False

class level_front(level_init_and_collision):
    def __init__(self, surface, level):
        super().__init__(surface, level)

    def parralax(self, pos, offset):
        for rect in self.arena: rect[0], rect[1] = move_rect(rect, pos, offset)
        self.path.update(pos, offset)
        self.decor.update(pos, offset)
        self.new_map.update(pos, offset)
        self.animd.update(pos, offset)
        self.png.update(pos, offset)
        self.anex.update(pos, offset)

    def all_collision_check(self, move):
        if self.is_colliding(self.lucas, self.decor, move)\
            or self.is_colliding(self.lucas, self.png, move)\
            or self.is_colliding(self.lucas,self.new_map, move):
            return True
        else:
            return False

    def play_move(self, key):
        if key[py.K_RIGHT] and self.all_collision_check('R') == False:
            self.dec[0] += 2
            self.parralax('R', 2)
            self.state = 6
        elif key[py.K_LEFT] and self.all_collision_check('L') == False:
            self.parralax('L', 2)
            self.dec[0] += 2
            self.state = 3
        elif key[py.K_UP] and self.all_collision_check('U') == False:
            self.parralax('U', 2)
            self.state = 9
        elif key[py.K_DOWN] and self.all_collision_check('D') == False:
            self.parralax('D', 2)
            self.state = 0

    def animate_grp(self, group):
        for elem in group: elem.play(0)

    def draw_map(self):
        self.path.draw(self.surface)
        self.decor.draw(self.surface)
        self.new_map.draw(self.surface)
        self.animd.draw(self.surface)
        self.png.draw(self.surface)
        self.anex.draw(self.surface)
        self.animate_grp(self.animd)
        self.animate_grp(self.png)

class level_fight_and_data(level_front):
    def __init__(self, surface, level):
        super().__init__(surface, level)

    def load_sortilege_enem(self):
        self.enemy_skills = []
        for enem in self.data_e:
            self.cursor.execute("""SELECT * FROM skill_m WHERE perso = ?;""", (enem[2],))
            result = self.cursor.fetchall()
            self.enemy_skills.append(result)

    def set_data(self, data):
        self.data = data
        self.guild = py.sprite.Group()
        x, y = 1200, 350
        for elem in data:
            spr = player(elem[1], [x, y], elem[-2], elem[-1], 0, elem)
            spr.set_size((100,100))
            self.guild.add(spr)
            y += 50

    def is_on_rect(self, rects, offset):
        pos = self.lucas.pos
        i = 0
        for elem in rects:
            if (self.is_inter(pos[0], elem[0], elem[0]+offset)
                and self.is_inter(pos[1], elem[1], elem[1]+offset)):
                self.to_drop = i
                return True
            i += 1
        return False

class level_fight_sequence(level_fight_and_data):
    def __init__(self, surface, level):
        super().__init__(surface, level)

    def load_sortilege(self, index):
        name = self.data[index][2]
        self.cursor.execute("""SELECT * FROM skill WHERE perso = ?;""", (name,))
        self.power_loaded = self.cursor.fetchall()
        x, y = 800, 400
        positions, size = [], []
        for elem in self.power_loaded:
            positions.append([x, y])
            size.append((250,60))
            y += 90
        self.select2 = cursor(size, positions, (240,204,40), 4)

    def kill_perso(self, group, cursor, data):
        if not group.sprites()[cursor.index].in_life():
            spr = group.sprites()[cursor.index]
            cursor.positions.pop(cursor.index)
            cursor.size.pop(cursor.index)
            data.pop(cursor.index)            
            cursor.index = 0
            group.remove(spr)

    def enem_fight(self):
        if is_empty(self.fg_enem) == False:
            index = random.randint(0, len(self.fg_enem.sprites())-1)
            skills = self.enemy_skills[index]
            index2 = random.randint(0, len(skills)-1)
            index3 = random.randint(0, len(self.guild)-1)
            skill = skills[index2]
            data_enem = skill[2:6]
            data_me = skill[6:10]
            self.fg_enem.sprites()[index].put_damage(data_enem, self.surface)
            self.guild.sprites()[index3].put_damage(data_me, self.surface)
            self.kill_perso(self.guild, self.select, self.data)
        self.status = "arena_me"

    def user_fight(self):
        pos = self.select2.index
        self.cursor.execute("""SELECT * FROM skill WHERE skills = ?""", (self.power_loaded[pos][1],))
        data_first = self.cursor.fetchall()[0]
        data_enem = data_first[3:7]
        data_me = data_first[7:11]
        self.fg_enem.sprites()[self.select3.index].put_damage(data_enem, self.surface)
        self.guild.sprites()[self.select.index].put_damage(data_me, self.surface)
        self.kill_perso(self.fg_enem, self.select3, self.data_e)

class png_sequence(level_fight_sequence):
    def __init__(self, surface, level):
        super().__init__(surface, level)

    def next_line(self):
        self.current = 1.0
        self.prev = 1
        self.line += 1
        self.txt_dis.text = ''
        self.len = len(self.talk[self.line])-1
        self.play_tlkin = int(self.talk[self.line][1])

    def event_diss(self, key):
        len2 = len(self.talk)-1
        if key == py.K_ESCAPE and self.status == 'diss': self.status = 'ext'
        if key == py.K_RETURN and self.status == 'diss' and self.line >= len2\
            and int(self.current) >= self.len:
            self.status = 'ext'
            self.is_contact = 0
        if key == py.K_RETURN and self.status == 'diss' and self.line < len2\
            and int(self.current) >= self.len:
            self.next_line()
        if key == py.K_TAB and self.status == 'diss':
            self.disc_offset = 0.3
        if key == py.K_BACKSPACE and self.status == 'diss':
            self.disc_offset = 0.08

    def load_diss_img(self, imgs):
        perso_list = imgs.split('\n', imgs.count('\n'))
        perso_list.pop(-1)
        self.perso_list = []
        for i in perso_list:
            spr = static_sprite(i, [1400, 400])
            spr.set_size([100,100])
            self.perso_list.append(spr)

    def load_diss_script(self, talk):
        self.talk = talk.split('/', talk.count('/'))
        self.talk.pop(-1)
        self.current = 1.0
        self.prev = 1
        self.play_tlkin = int(self.talk[0][1])
        self.txt_dis = text('font/med2.ttf', '', (255,255,255), 30)
        self.line = 0
        self.disc_offset = 0.08
        self.len = len(self.talk[0])-1

    def load_diss(self):
        self.status = 'diss'
        target = self.png_info[self.is_contact-1]
        content = get_file(target)
        imgs, talk = content.split('@', 1)
        self.load_diss_img(imgs)
        self.load_diss_script(talk)

    def manage_dis(self):
        self.surface.blit(self.dis_bg.image, self.dis_bg.rect)
        self.dis_bg.play(0)
        if (int(self.current) > self.prev):
            self.prev = int(self.current)
            self.txt_dis.text += self.talk[self.line][self.prev]
        if (int(self.current) < self.len): self.current += self.disc_offset            
        spr = self.perso_list[self.play_tlkin]
        self.txt_dis.draw(self.surface, [450, 520])
        self.surface.blit(spr.image, spr.rect)

class to_new_level(png_sequence):
    def __init__(self, surface, level):
        super().__init__(surface, level)

    def set_the_portal(self):
        self.snd_game.stop()
        target = self.portal_info[self.new_contact-1]
        self.__init__(self.surface, target)
        self.set_cursor(self.cursor)
        self.init_map()
        self.snd_game.play(-1)

class level_inventaire(to_new_level):
    def __init__(self, surface, level):
        super().__init__(surface, level)
        self.new_contact = False

    def event_invent(self, key):
        if key == py.K_RIGHT: self.invent_cursor.move_hori(True)
        if key == py.K_LEFT: self.invent_cursor.move_hori(False)
        if key == py.K_UP: self.invent_cursor.move_verti(False)
        if key == py.K_DOWN: self.invent_cursor.move_verti(True)

class level_manager(level_inventaire):
    def __init__(self, surface, level):
        super().__init__(surface, level)

    def manage_ext_state(self):
        x, y = self.lucas.pos
        key = py.key.get_pressed()
        x += 5; y -= 40
        self.lucas.play(self.state)
        self.draw_map()
        self.surface.blit(self.lucas.image, self.lucas.rect)
        if self.is_on_rect(self.arena, 50): self.init_fight()
        self.play_move(key)
        if any(key):
            self.is_contact = self.is_png()
            self.new_contact = self.is_portal()
        if self.is_contact or self.new_contact:
            txt = text('font/med2.ttf', "Click enter for info", (255,255,255), 20)
            py.draw.rect(self.surface, (0,0,0), ((x, y), (160, 30)), 0)
            txt.draw(self.surface, [x, y])

    def arena_me_manager(self):
        self.surface.blit(self.fg_grd.image, self.fg_grd.rect)
        self.surface.blit(self.fg_bg.image, self.fg_bg.rect)
        self.guild.draw(self.surface)
        self.fg_enem.draw(self.surface)
        self.select.draw(self.surface)
        for i in self.guild:
            print(i.inc_speed)
            i.play(0)
            i.put_xp(self.surface)
        for i in self.fg_enem:
            i.play(0)
            i.put_xp(self.surface)

    def draw_the_sortilege(self):
        x, y = 800, 400
        for elem in self.power_loaded:
            py.draw.rect(self.surface, (0,0,0), ((x, y), (250, 60)), 0)
            txt = text('font/med2.ttf', elem[1], (255,255,255), 30)
            txt.draw(self.surface, [x+10, y])
            y += 90
        self.select2.draw(self.surface)

    def move_the_select_cursor(self, key, cursor):
        if key == py.K_DOWN: cursor.move_hori(True)
        if key == py.K_UP: cursor.move_hori(False)

    def manage_arena_state(self):
        if self.status == "arena_me":
            if is_empty(self.fg_enem) or is_empty(self.guild):
                self.arena.pop(self.to_drop)
                self.snd_fg.stop()
                self.snd_game.play(-1)
                self.status = 'ext'
            self.arena_me_manager()
        if self.status == 'arena_select':
            self.arena_me_manager()
            self.draw_the_sortilege()
        if self.status == 'arena_select2':
            self.arena_me_manager()
            self.draw_the_sortilege()
            self.select3.draw(self.surface)
        if self.status == 'arena_enem':
            self.arena_me_manager()
            self.enem_fight()
