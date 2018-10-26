################################
# Escaner de puertos en python #
########## braulio23 ###########
###### foro.elhacker.net #######
################################
import socket

print "Escaner de puertos by braulio23\n"
host = "172.2.25.142"
puerto = 6080
socket = socket.socket()

try:
    socket.connect((host, puerto))
    print "Puerto " + str(puerto) + " abierto"
    socket.close()
except:
    print "Puerto " + str(puerto) + " cerrado."
