#! /usr/bin/env python

from os import system
from urllib2 import urlopen
from socket import socket
from sys import argv
from time import asctime
import smtplib
import string
from ftplib import FTP
from threading import Timer

#ejemplo de uso:
#python server_monitoring.py http myBlog  http://myblog.com
#python server_monitoring.py ftp  myFtpServer ftp_ip ftp_user ftp_pwd

FROM = "my_monitor@mymail.com"
TIMEOUT = 5
HOST = "myMailServer"
emails = ["user1@mymail.com", "user2@mymail.com"]

def tcp_test(argv):
    cpos = server_info.find(':')
    try:
	server_url = argv[3]
        sock = socket()
        sock.connect((server_info[:cpos], int(server_url[cpos+1:])))
        sock.close
    except:
	send_error(argv, e)

def http_test(argv):
    try:
	server_url = argv[3]
        data = urlopen(server_url, None, TIMEOUT).read()
    except  Exception as e:
	print e
	send_error(argv, e)

def ftp_test(argv):
    try:
	server_url = argv[3]
	user = argv[4]
	pwd = argv[5]
        ftp = FTP(server_url, user, pwd, None, TIMEOUT)
        ftp.quit()
    except Exception as e:
	print e
	send_error(argv, e)

def server_test(argv ):
    test_type = argv[1]
    if test_type.lower() == 'tcp':
        tcp_test(argv)
    elif test_type.lower() == 'http':
        http_test(argv)
    elif test_type.lower() == 'ftp':
        ftp_test(argv)


def send_error(argv, error):
    test_type = argv[1]
    service_name = argv[2]
    server_url	 = argv[3]

    subject = 'Error de Monitoreo en el Servidor: %s: %s %s ( %s ) ' % (service_name, asctime(), test_type.upper(), server_url)
    message = 'Error al realizar monitoreo al servidor  %s \r\n Tipo de Servicio: %s  \r\n Tipo de Error: %s \r\n Direccion del servicio : %s ' % (service_name, test_type.upper(), error, server_url)

    TO = ', '.join( emails )
    BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % subject ,
        "",
        message
        ), "\r\n")
    server = smtplib.SMTP(HOST)
    server.sendmail(FROM, emails, BODY)
    server.quit()



if __name__ == '__main__':
    if len(argv) < 3:
        print('Wrong number of arguments.'+str(argv))
    else:
        pass

        argv= ["http" ,"sismos",  "http://srvags.sgc.gov.co/arcpro/rest/services/Geologia/Exploracion_Geologica_de_Fosfatos_Bloque_Boyaca_PL191_y_210/MapServer"]
    server_test(argv)