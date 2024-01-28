#!/usr/bin/env python3
##
## EPITECH PROJECT, 2023
## dual_realm
## File description:
## dual_realm
##

import pygame as py
from my_game_object import final_game_obj
from init_market_db import init_my_db
import sqlite3 as db

connect = db.connect('player.db')
cursor = connect.cursor()

py.init()

screen = py.display.set_mode((1900, 1000))
py.display.set_caption("Symphony of Dual Realm")
icone = py.image.load("./ressources/menu/king_back/frame_000_delay-0.03s.gif")
py.display.set_icon(icone)

init_my_db(cursor)
Game = final_game_obj('ressources/menu/king_back', True, screen, cursor)

Game.run()

connect.commit()
connect.close()

py.quit()