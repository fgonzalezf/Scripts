import arcpy,os, sys
import xml.etree.ElementTree as ET
FeatClass = r"C:\Users\pache\Documents\SGC\Metadatos\Modelo\MIIG.gdb\Metadato_Geografico\METADATO_MIIG_POL"
arcpy.env.workspace=FeatClass

XMLModelo = r=r"C:\Users\pache\Documents\SGC\Metadatos\Modelo\Modelo.xml"
XMLSalida = r"C:\Users\pache\Documents\SGC\Metadatos\Modelo\Prueba1"

tree = ET.parse(XMLModelo)
root = tree.getroot()

#variables Metadato
identificador=None
fechaMetadato=None
titulo=None
fechaPublicacion=None
resumen=None
palabrasClaves=None
oeste=None
este=None
sur=None
norte=None
url=None

for elem in root:
    if elem.tag=="{http://www.isotc211.org/2005/gmd}fileIdentifier":
        identificador=elem[0]
        print(elem[0].text)#identificador
    elif elem.tag=="{http://www.isotc211.org/2005/gmd}dateStamp":
        fechaMetadato=elem[0]
        print(elem[0].text)#fecha publicación geoportal
    elif elem.tag=="{http://www.isotc211.org/2005/gmd}identificationInfo":
        titulo=elem[0][0][0][0][0]
        print(elem[0][0][0][0][0].text)# Titulo
        fechaPublicacion=elem[0][0][0][1][0][0][0]
        print(elem[0][0][0][1][0][0][0].text)# fecha publicacion
        resumen=elem[0][1][0]
        print(elem[0][1][0].text)# Abstract
        palabrasClaves=elem[0][4][0][0][0]
        print(elem[0][4][0][0][0].text)# palabras claves
        oeste=elem[0][8][0][0][0][0][0]
        print(elem[0][8][0][0][0][0][0].text)  # Oeste
        este=elem[0][8][0][0][0][1][0]
        print(elem[0][8][0][0][0][1][0].text)  # este
        sur=elem[0][8][0][0][0][2][0]
        print(elem[0][8][0][0][0][2][0].text)  # Sur
        norte=elem[0][8][0][0][0][3][0]
        print(elem[0][8][0][0][0][3][0].text)  # Norte
    elif elem.tag == "{http://www.isotc211.org/2005/gmd}distributionInfo":
        url=elem[0][1][0][0][0][0][0]
        print(elem[0][1][0][0][0][0][0].text)  # URL

#recorrer base de datos
fields=["IDENTIFICADOR_DEL_METADATO",#0
        "TÍTULO_DEL_RECURSO",#1
        "AREA_DEL_CONOCIMIENTO",#2
        "FECHA_DE_PUBLICACION",#3
        "URL_RECURSO",#4
        "COORDENADA_GEOGRAFICA_OESTE",#5
        "COORDENADA_GEOGRAFICA_ESTE",#6
        "COORDENADA_GEOGRAFICA_SUR",#7
        "COORDENADA_GEOGRAFICA_NORTE"]#8
Count=0
with arcpy.da.SearchCursor(FeatClass, fields) as cursor:
    for row in cursor:
        identificador.text=row[0]
        titulo.text=row[1]
        resumen.text=row[1]
        palabrasClaves.text=row[2]
        fechaPublicacion.text=str(row[3])
        url.text=str(row[4])
        oeste.text=str(row[5])
        este.text=str(row[6])
        sur.text=str(row[7])
        norte.text=str(row[8])
        print(str(row[8]))
        Count=Count+1
        tree.write(XMLSalida+os.sep+"Metadato_"+str(Count)+".xml",encoding='utf-8')






