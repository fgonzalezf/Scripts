__author__ = 'fernando.gonzalez'
from reportlab.pdfgen import canvas

def hello(c):
    c.drawString(100,100,"Hola")

c=canvas.Canvas(r"X:\PRUEBAS\PDF\hola.pdf")
hello(c)
c.showPage()
c.save()