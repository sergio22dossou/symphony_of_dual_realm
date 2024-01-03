#!/usr/bin/env/ python3

LVL = {' ':"ressources/lvl1/grass.png", 't':"ressources/lvl1/tree.png", 's':"ressources/lvl1/sand.png", '@':"ressources/lvl1/hole.png", 'h':"ressources/lvl1/home.png", "p":"ressources/lvl1/puits.png", 'r':"ressources/lvl1/rock.png", "e":"ressources/lvl1/Water", "T":"ressources/lvl1/tree2.png", 'b':"ressources/lvl1/bridge.png", ":":"ressources/lvl1/rock2.png", "=":"ressources/lvl1/design.png", "P":"ressources/lvl1/Joffrey"}
LVL_scale = {' ':(50, 50), 't':(60, 60), 's':(100, 100), '@':(100, 100), 'h':(190, 190), 'p':(70, 70), 'r':(55, 55), 'T':(60,60), 'b':(60,60),'e':(50,50), ':':(50,50), '=':(60,60), 'P':(50,50)}
LVL_group = {' ':"path", 't':"decor", 's':"path", '@':"new_map", 'h':"new_map", 'p':"decor", 'r':"decor", 'T':"decor", 'b':"path", 'e':"animd", ':':"decor", "=":"path", 'P':"png"}
animated = ['e', 'P']
animd_keys = {'e':(0.04, 2, 0), 'P':(0.05, 2, 0)}
static = [' ', 't', 's', 'r', 'p', 'T', 'b', ':', '=', 'h', '@']

png_script = ["./script/lvl1/first_conv.txt"]