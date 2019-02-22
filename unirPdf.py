#!/usr/bin/python
# -*- coding: utf-8 -*-
import  os, sys
from pyPdf import PdfFileWriter, PdfFileReader

# Creamos una funcion que automatice la union de los archivos pdf
def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

# Instanciamos la escritura de archivos PDF de la libreria pypdf
output = PdfFileWriter()

# AÃ±adimos los reportes, estos podemos cargarlos desde archivos temporales
append_pdf(PdfFileReader(file(r"C:\Users\fgonzalezf\Downloads\Epis\Hoja_de_vida-1-5.pdf","rb")),output)
append_pdf(PdfFileReader(file(r"C:\Users\fgonzalezf\Downloads\Epis\Hoja1.pdf","rb")),output)


# Escribimos la Salida Final del Reporte
output.write(file(r"C:\Users\fgonzalezf\Downloads\Epis\Hoja7.pdf","wb"))


