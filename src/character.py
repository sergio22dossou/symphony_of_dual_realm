import pygame as py
from static_sprite import static_sprite
from anim_sprite import animd_sprite
from text_and_button import text


RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

class player(animd_sprite):
    def __init__(self, dir_name, pos, inc_speed, max_size, offset, data):
        super().__init__(dir_name, pos, inc_speed, max_size, offset)
        self.name = data[2]
        self.type = data[3]
        self.vit = data[4]
        self.life = data[5]
        self.res = data[6]
        self.pv = data[7]
        self.active_life = self.life
        self.active_pv = self.pv
        self.active_vit = self.vit
        self.active_res = self.res
        self.size = self.life // 3

    def put_xp(self, screen):
        x, y = self.pos
        x += 180
        y += 20
        color = None
        if self.active_life < self.size:
            color = RED
        elif self.active_life > self.size and self.active_life < self.size*2:
            color = YELLOW
        else:
            color = GREEN
        txt = text('font/med2.ttf', "pv", (255,255,255), 20)
        txt2 = text('font/med2.ttf', "life", (255,255,255), 20)
        py.draw.rect(screen, (0,0,0), ((x, y), (self.pv*2,20),))
        py.draw.rect(screen, BLUE, ((x, y), (self.active_pv*2,20)))
        txt.draw(screen, [x-50,y])
        y += 50
        txt2.draw(screen, [x-50,y])
        py.draw.rect(screen, (0,0,0), ((x, y), (self.life*2,20)))
        py.draw.rect(screen, color, ((x, y), (self.active_life*2,20)))

    def in_life(self):
        if self.active_life > 0:
            return True
        else:
            return False

    def put_damage(self, data, screen):
        self.active_vit += data[0]
        self.active_life += data[1]
        self.active_res += data[2]
        self.active_pv += data[3]

class badguy(animd_sprite):
    def __init__(self, dir_name, pos, inc_speed, max_size, offset, data):
        super().__init__(dir_name, pos, inc_speed, max_size, offset)
        self.name = data[2]
        self.grade = data[0]
        self.vit = data[3]
        self.life = data[4]
        self.res = data[5]
        self.pv = data[6]
        self.active_life = self.life
        self.active_pv = self.pv
        self.active_vit = self.vit
        self.active_res = self.res
        self.size = self.life // 3


    def put_xp(self, screen):
        x, y = self.pos
        x -= 120
        y += 40
        color = None
        if self.active_life < self.size:
            color = RED
        elif self.active_life > self.size and self.active_life < self.size*2:
            color = YELLOW
        else:
            color = GREEN
        txt = text('font/med2.ttf', "pv", (255,255,255), 20)
        txt2 = text('font/med2.ttf', "life", (255,255,255), 20)
        py.draw.rect(screen, (0,0,0), ((x, y), (self.pv*2,20)))
        py.draw.rect(screen, BLUE, ((x, y), (self.active_pv*2,20)))
        txt.draw(screen, [x-50,y])
        y += 40
        txt2.draw(screen, [x-50,y])
        py.draw.rect(screen, (0,0,0), ((x, y), (self.life*2,20)))
        py.draw.rect(screen, color, ((x, y), (self.active_life*2,20)))

    def in_life(self):
        if self.active_life > 1:
            return True
        else:
            return False

    def put_damage(self, data, screen):
        self.active_vit += data[0]
        self.active_life += data[1]
        self.active_res += data[2]
        self.active_pv += data[3]