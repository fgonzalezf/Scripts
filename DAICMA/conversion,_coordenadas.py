# -*- coding: utf-8 -*-
import re, os

X="""71º 49' 57" W"""
temp=""
for y in X:

    if (y in ['0','1','2','3','4','5','6','7','8','9'," ","N","W"]):
        temp=temp+y
Numeros=temp.split(" ")
decimal=0.0
if Numeros[3]=="N":
    decimal = float(Numeros[0])+float(Numeros[1])/60+float(Numeros[2])/3600
else:
    decimal = (-1)*float(Numeros[0]) - float(Numeros[1]) / 60 -float(Numeros[2]) / 3600

print decimal