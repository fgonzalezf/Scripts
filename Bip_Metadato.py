#-*- coding: utf-8 -*-
import arcpy, os, sys, sqlite3, json,time

def MetadatoConstante( **parametros):
    dic={}
    for parametro in parametros:
        dic[parametro]=[str((parametros[parametro]))]
    return dic

def convertirDato(key, dato, form,nomform):
    datofinal = ""
    for dto in dato:
        datofinal = datofinal + dto + ","
    form.fields[nomform].initial = datofinal[:-1]
def convertirDatoNum(key, dato, form,nomform):
    datofinal = 0
    for dto in dato:
        datofinal =  float(dto.replace(",","."))
    form.fields[nomform].initial = datofinal
def convertirDate(datoin):
    datofinal = ""
    dato = str(datoin).split(" ")[0]
    datofinal = dato.split("-")[2]+"/"+dato.split("-")[1]+"/"+dato.split("-")[0]
    return datofinal

def convertirFloat(datoin):
    datofinal = ""
    dato = str(datoin)
    datofinal = dato.replace(".",",")
    return datofinal

def metadatovariable(metadatoConstante,**parametros):
    dic = metadatoConstante
    for parametro in parametros:
        dic[parametro] = [str((parametros[parametro]))]
    return dic

Tabla=r"C:\Users\Desarrollo\Documents\Bip_Metadato\Tablas.mdb\Metadato"
con =sqlite3.connect(r'C:\Users\Desarrollo\Documents\Bip_Metadato\MOAI.db')

cursorSQL=con.cursor()

METADATO_CONSTANTE=MetadatoConstante(
AreaConocim="Hidrocarburos",
BusqPredef=" ",
Depart="No definido",
DescMetEvMet="Método de evaluación de la calidad basado en la inspección de "
             "la cantidad de valores de atributos de metadatos diligenciados respecto a la cantidad de "
             "atributos de metadatos definidos en el esquema de metadatos al que pertenece el recurso",
DescripMedidMet="Cantidad de atributos de metadatos diligenciados respecto al esquema de metadatos definido",
DescripMedidMetConsLog="Valores de atributos de metadatos diligenciados corresponden a la abstracción del universo de conjunto de datos",
EscalaProy="Sin Escala Definida",
EstadProyect="Sin definir",
LineaTemat="Banco de Información Petrolera",
Municip="No definido",
NombMedMet="Calidad del contenido de valores de atributos de metadatos diligenciados",
NombrMedMet="Totalidad de atributos de metadatos diligenciados",
PlancIGAC="No definido",
PorcentComplet="Sin definir",
TipEvaluaMetConsDom="Directo Interno",
TipoResult="Objetos Geográficos",
UnidMedValorMetConsDom="No definido",
UnidadMedValMet="No aplica",
ValorCalMeConsDom="Muy Bueno: Los valores de atributos de  metadatos están actualizados respecto al conjunto de datos fuente",
ValorMetad="Completo  (los atributos de metadatos contienen valor diligenciado respecto al esquema de metadatos)",
VistConcep="No definido",
accessConstraints="De uso Publico",
accessConstraints1="De uso Publico",
administrativeArea="Bogotá D.C.",
administrativeArea1="Bogotá D.C.",
administrativeArea2="Bogotá D.C.  (Departamento de Cundinamarca)",
associationType="No aplica",
characterSet="utf8",
characterSet1="utf8",
city="Bogotá D.C.",
city1="Bogotá D.C.",
city2="Bogotá D.C.",
classification="No Clasificado",
classification1="No Clasificado",
contributor="Servicio Geológico Colombiano SGC Diagonal 53 No. 34 - 53",
country="Colombia",
country1="Colombia",
country2="Colombia",
creator="Servicio Geológico Colombiano",
dataset="No definido",
date3="Sin Definir",
date4="Sin Definir",
deliveyPoint1="Diagonal 53 No. 34 - 53",
deliveyPoint2="Diagonal 53 No. 34 - 53",
denominator="1",
description4="No aplica",
description5="Enlace de acceso al recurso geocientífico",
descriptionReferenceSystem="WGS-84",
distance="No aplica",
electronicMailAddress="sgc_epis.dir@sgc.gov.co",
electronicMailAddress1="sgc_epis.dir@sgc.gov.co",
electronicMailAddress2="sgc_epis.dir@sgc.gov.co",
fees="Información sin costo monetario",

format="SHP",

language="spa",
language1="spa",
level="Conjunto de datos",
maintenanceAndUpdateFrequency="Script diario de actualización",
maintenanceNote="Datos actualizados diariamente",
metadataStandardName="Esquema (perfil) de metadato adoptado y adaptado  para el SGC a partir de la Norma Técnica Colombiana NTC-4611 Segunda Actualización del 13/04/2011",
metadataStandardVersion="Version 1",
name1="URL de enlace",
otherConstraints="No definido",
otherConstraints1="No definido",
postalCode="111321",
postalCode1="111321",
postalCode2="111321",
prodImpr="No aplica",
protocol="Dirección Web (URL-Uniforme Resourse Locators)",
publisher="Servicio Geológico Colombiano - SGC  Sede Principal.   Grupo de Participación Ciudadana y Comunicaciones",
publisher1="Servicio Geológico Colombiano - SGC  Sede Principal.   Grupo de Participación Ciudadana y Comunicaciones",
purpose="Administración Información BIP",
relation="Para información detalla consultar con el area de Suministro",
rights="""El usuario reconoce que la información geocientífica a que tenga acceso es de propiedad o custodia del "
       "Servicio Geológico Colombiano \u2013 SGC de conformidad con la ley 23 de 1982, la decisión 351 de 1993, ley 44 de 1993 "
       "y demás normas relacionadas con la propiedad intelectual.  Por lo anterior al usuario no le asiste ningún derecho de "
       "propiedad intelectual, sin que se entiendan cedidos o licenciados a ningún título.Este recurso contiene Información "
       "geocientífica que permite conocer el subsuelo colombiano.   El SGC fundamenta su política de Propiedad Intelectual con los "
       "siguientes criterios:1-La información geocientífica del SGC debe ser sujeto de protección de la propiedad intelectual:  "
       "Se considera la información geocientífica del SGC básica o temática, análoga o digital como una creación "
       "original, por lo cual no podrá reproducirse total o parcialmente sin el permiso expreso de una autoridad institucional debidamente "
       "acreditada, aún si no se está reproduciendo con propósitos comerciales.2-Derechos de carácter personal o derechos "
       "moralesEl SGC reconoce que los derechos de carácter personal sobre una creación de información geocientífica son "
       "irrenunciables e inalienables y perpetuos. Para ello destaca el derecho al reconocimiento de la condición de autor de la obra o del "
       "reconocimiento e inclusión apropiada del nombre del autor intelectual de los datos institucionales y el de exigir el respeto a la "
       "integridad de la obra o actuación y la no alteración de las mismas que pueda ir en detrimento de su honor o "
       "reputación.3-Derechos de carácter patrimonialEl SGC tendrá el derecho exclusivo de realizar o de autorizar uno "
       "cualquiera de los actos siguientes: Reproducir la obra. Efectuar una traducción, una adaptación, un arreglo o cualquier "
       "otra transformación de la obra. Comunicar la obra al público mediante la representación, ejecución, radiodifusión "
       "o por cualquier otro medio.El SGC distingue los derechos de carácter patrimonial como aquéllos relacionados con:  a)    "
       "Explotación de la obra o prestación protegida, que a su vez se subdividen en derechos exclusivos y en derechos de simple "
       "remuneración: Los derechos exclusivos sobre los datos institucionales son únicamente del SGC y no serán dados a terceros. "
       "Los derechos de simple remuneración, también conocidos bajo la denominación de \licencias de uso\", son aquellos que el SGC "
       "concede a determinados licenciados, en virtud de los cuales se exige a la persona que explota su obra o prestación "
       "protegida el pago de una suma de dinero. Estos derechos, frente a los \"exclusivos\" son considerados \"menores\". "
       "b) Derechos meramente compensatorios, como el derecho por copia privada que compensa los derechos de propiedad intelectual "
       "dejados de percibir por razón de las reproducciones de las obras o prestaciones protegidas para uso exclusivamente "
       "privado del usuario.4- Garantía de los derechos morales de los autores y patrimoniales del SGCEl SGC garantizará "
       "los derechos morales de los autores, así como los derechos patrimoniales sobre la información geocientífica "
       "que ostenta el SGC y  las entidades productoras que hayan entregado conjuntos de datos en custodia del SGC, mediante el concurso "
       "de la Dirección Nacional de Derechos de Autor del Ministerio del Interior o quién haga sus veces.5- Infracciones "
       "Toda modificación o adición no autorizada que un usuario realice al conjunto de datos o producto de información "
       "suministrado por el SGC se considera una infracción a los derechos de propiedad intelectual, a menos de que la información "
       "haya sido provista directamente por el SGC, se le reconozca como fuente y cuyo propósito de la modificación sea "
       "con autorización previa del SGC para: Corrección de errores sobre el conjunto de datos, o derivar trabajos resultado "
       "de trabajos originales, o Investigación, o estudios privados o personales, o creación de copias de seguridad.""",
role="Autor",
role1="Punto de Contacto",
role2="Punto de Contacto",

spatialRepresentationType="Tabla de Texto",
statement="No definido",
status="Servicio",


topicCategory="Información Geocientífica",
type="No Definido",
type1="Tema",
useConstraints="De uso Publico",
useConstraints1="De uso Publico",
usernote="No definido",
version="No aplica",
voice="(571) 2200200-3037 - lunes a viernes 8.00 a.m. a 5 p.m. para todas nuestras sedes.",
voice1="(571) 2200200-3037 - lunes a viernes 8.00 a.m. a 5 p.m. para todas nuestras sedes.",
voice2="(571) 2200200-3037 - lunes a viernes 8.00 a.m. a 5 p.m. para todas nuestras sedes.",

DescripMetEvConsDom="Método de evaluación de la calidad basado en la inspección del contenido de valores de atributos de metadatos diligenciados pertinentes  respecto al universo del conjunto de datos",
TipEvaluaMet="Directo Externo",
ZonaPais="No definido",
source=" ",

)
def ConvertToJSon( metadato,**parametros):
    dic= metadato
    for parametro in parametros:
            dic[parametro]=(parametros[parametro]).encode('utf-8').split(";")
    stringJson =json.dumps(dic,separators=(',', ': '),sort_keys=True)
    return stringJson

Campos=["record_id","fileName","identifier","identifier1",
        "source1","subject","title1","title","abstract","date_","date1","date2","dateType","datestamp","datestamp1",
        "datestamp2","description1","eastBoundLongitude","northBoundLatitude","southBoundLatitude","westBoundLongitude","path"]


with arcpy.da.SearchCursor(Tabla, Campos) as cursor:
    for row in cursor:
        metadata= ConvertToJSon(METADATO_CONSTANTE,
        fileName=row[1],
        identifier=row[2],
        identifier1=row[3],
        source1=row[4],
        subject=row[5],
        title1=row[6],
        title=row[7],
        abstract=row[8],
        date=str(row[9]).split("/")[2]+"-"+str(row[9]).split("/")[1]+"-"+str(row[9]).split("/")[0],
        date1=row[10],
        date2=row[11],
        dateType=row[12],
        datestamp=row[13],
        datestamp1=row[14],
        datestamp2=row[15],
        description1=row[16],
        eastBoundLongitude=str(row[17]).replace(".",","),
        northBoundLatitude=str(row[18]).replace(".",","),
        southBoundLatitude=str(row[19]).replace(".",","),
        westBoundLongitude=str(row[20]).replace(".",","),
        path=row[21]
        )

        try:
            cursorSQL.execute('INSERT INTO records (record_id , modified, metadata) VALUES ('+'"'+str(row[0]) + '"'+",'" + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + "','" + metadata + "')")
            cursorSQL.execute("INSERT INTO setrefs (record_id , set_id) VALUES ("+'"'+str(row[0])+ '"'+",'geoportal')")
        except:
            llave = str(row[0])
            metadato = metadata
            cursorSQL.execute('''UPDATE records SET metadata = ? WHERE record_id = ? ''', (metadato, llave))

        con.commit()
        print str(row[0])

print "coneccion"

con.close()


