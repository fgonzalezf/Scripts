################################
# Escaner de puertos en python #
########## braulio23 ###########
###### foro.elhacker.net #######
################################
import socket
import win32serviceutil
import time



import os

import win32serviceutil

print "Escaner de puertos by braulio23\n"
host = "localhost"
puerto = 6080
socket = socket.socket()
TXT=r"C:\temp\LodReiniciosArcgisServer.txt"
def logResultado():
    ahora = time.strftime("%c")
    f = open(TXT, 'w')
    f.write("ArcGis Server reiniciado........ " + ahora + "\n")
    f.close()

try:
    socket.connect((host, puerto))
    print "Puerto " + str(puerto) + " abierto"
    socket.close()
except:

    print "Puerto " + str(puerto) + " cerrado."
    serviceName = "ArcGIS License Manager"
    win32serviceutil.RestartService(serviceName)
    print "Servicio Reiniciado"
    logResultado()
