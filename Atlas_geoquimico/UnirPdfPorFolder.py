from os import walk
import os
import  os, sys
from pyPdf import PdfFileWriter, PdfFileReader

def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

def ls(ruta = '.'):
    dir, subdirs, archivos = next(walk(ruta))

    for sub in subdirs:
        subCarpeta= ruta+ os.sep+ sub
        print subCarpeta
        dir1, subdirs1, archivos1= next(walk(subCarpeta))
        output = PdfFileWriter()
        for arcpdf in archivos1:
            if ".pdf" in arcpdf:
                print arcpdf
                archivopdf=subCarpeta+os.sep+arcpdf
                append_pdf(PdfFileReader(file(archivopdf, "rb")),output)
        salida=subCarpeta+os.sep+sub+".pdf"
        output.write(file(salida, "wb"))
ls(r"G:\Atlas_geoquimico_2018\AGC_2018_Pdf")