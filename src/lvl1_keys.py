#!/usr/bin/env/ python3

LVL = {' ':"./lvl1/grass.png", 't':"./lvl1/tree.png", 's':"./lvl1/sand.png", '@':"./lvl1/hole.png", 'h':"./lvl1/home.png", "p":"lvl1/puits.png", 'r':"lvl1/rock.png"}
LVL_scale = {' ':(50, 50), 't':(60, 60), 's':(70, 70), '@':(100, 100), 'h':(190, 190), 'p':(70, 70), 'r':(60, 60)}
LVL_group = {' ':"path", 't':"decor", 's':"path", '@':"enemy", 'h':"dynamc_obj", 'p':"decor", 'r':"decor"}
group = ["path", "decor", "dynamc_obj", "anex", "enemy"]
static = [' ', 't', 's', 'r', 'p']