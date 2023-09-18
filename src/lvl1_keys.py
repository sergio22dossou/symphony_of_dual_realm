#!/usr/bin/env/ python3

LVL = {' ':"ressources/lvl1/grass.png", 't':"ressources/lvl1/tree.png", 's':"ressources/lvl1/sand.png", '@':"ressources/lvl1/hole.png", 'h':"ressources/lvl1/home.png", "p":"ressources/lvl1/puits.png", 'r':"ressources/lvl1/rock.png"}
LVL_scale = {' ':(50, 50), 't':(60, 60), 's':(70, 70), '@':(100, 100), 'h':(190, 190), 'p':(70, 70), 'r':(60, 60)}
LVL_group = {' ':"path", 't':"decor", 's':"path", '@':"enemy", 'h':"dynamc_obj", 'p':"decor", 'r':"decor"}
group = ["path", "decor", "dynamc_obj", "anex", "enemy"]
static = [' ', 't', 's', 'r', 'p']