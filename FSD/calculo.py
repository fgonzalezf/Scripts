import os

def calculo(cor):
    temp=cor.strip()
    grados=int(temp.split("°")[0].strip())
    minutos=int(temp.split("°")[1].split("'")[0].strip())
    segundos= float(temp.split("'")[1].split('"')[0].strip().replace(",","."))
    decimal=grados + (minutos/60) + (segundos/3600)
    return decimal