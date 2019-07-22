# -*- coding: utf-8 -*-
import re, os,datetime,shutil

X="""71º 49' 57" W"""
temp=""
def convertDecimal(textoSexagesimal):
    for y in textoSexagesimal:

        if (y in ['0','1','2','3','4','5','6','7','8','9'," ","N","W"]):
            temp=temp+y
    Numeros=temp.split(" ")
    decimal=0.0
    if Numeros[3]=="N":
        decimal = float(Numeros[0])+float(Numeros[1])/60+float(Numeros[2])/3600
    else:
        decimal = (-1)*float(Numeros[0]) - float(Numeros[1]) / 60 -float(Numeros[2]) / 3600
    return float(decimal)
def copiarRenombrar(rutaVieja):
    carpetaNueva= r"C:\Temp"
    fechaHoy =datetime.datetime.now()
    strFecha=fechaHoy.strftime('%Y%m%d%H%M%S')
    shutil.copy(rutaVieja,carpetaNueva)
    os.rename(carpetaNueva+os.sep+os.path.basename(rutaVieja), carpetaNueva+os.sep+strFecha+".xlsx")
    print strFecha
copiarRenombrar(r"C:\Users\APN\Downloads\CENAM_MODELO.xlsx")