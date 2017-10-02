#!/usr/bin/env python
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


con =sqlite3.connect(r'C:\Users\Equipo\Documents\matadato_BIP\MOAI.db')

cursor=con.cursor()

METADATO_CONSTANTE=MetadatoConstante(
AreaConocim="Hidrocarburos",
BusqPredef=" ",
Depart="No definido",
DescMetEvMet="Método de evaluación de la calidad basado en la inspección de "
             "la cantidad de valores de atributos de metadatos diligenciados respecto a la cantidad de "
             "atributos de metadatos definidos en el esquema de metadatos al que pertenece el recurso",
DescripMedidMet="Cantidad de atributos de metadatos diligenciados respecto al esquema de metadatos definido",
DescripMedidMetConsLog="Valores de atributos de metadatos diligenciados corresponden a la abstracción del universo de conjunto de datos",
EscalaProy="0,0423611111111111",
EstadProyect="Sin definir",
LineaTemat="BIP",
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
fileName="http://srvags.sgc.gov.co/JSViewer/GEOVISOR_BIP/",
format="SHP",
identifier="http://srvags.sgc.gov.co/JSViewer/GEOVISOR_BIP/",
identifier1="http://srvags.sgc.gov.co/JSViewer/GEOVISOR_BIP/",
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
source1="http://srvags.sgc.gov.co/JSViewer/GEOVISOR_BIP/",
spatialRepresentationType="Tabla de Texto",
statement="No definido",
status="Servicio",
subject="Cuenca, Pozo, Colombia,petroleo, BIP, hidrocarburos",
title1="Banco de Información Petrolero",
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
title="Información EPIS de la Cuenca SINU-SAN JACINTO",
abstract="La cuenca SINU-SAN JACINTO Tiene: 66 Contratos y 241 Pozos, de los cuales 155 están disponibles en el Servicio Geológico, el listado de los pozos es el siguiente: CHINU-4 / CHINU-6 / P6-3S HACIENDA LA ESTANCIA / LOS ANGELES-12 / BULLERENGUE-1 / CURRULAO-1 / P-5  CARACOLI / BARU-1 / P-7 ARROYO ARENA / COLONCITOS-1 / CORRALITO-1 / EL CARMEN-1 (ZAMBRANO-1) / EL CARMEN-2 / PORQUERA-1 / SAN JACINTO-1 (ZAMBRANO-2) / SAN JACINTO-2 / ANH-LA-CANTERA-1 / TURBACO-1 / ANH-VILLANUEVA-1 / TURBACO-2 / TURBACO-3 / TURBACO-4 / TURBACO-6 / PCH-1 / P-15 EL CONTENTO / P-26 VEREDA EL PALMAR / P-28 FINCA VILLA HERMOSA / P-16 FINCA EL PARAISO / P-18 FINCA VILLA AURA / P-13 NUEVA ESTRELLA / P-11  SAN SEBASTIAN / P-27 VEREDA LAS PINTURAS / ANH SSJ-10 ST R S / ANH SSJ-2 ST R S / ANH SSJ-4 ST R S / ANH SSJ-4A ST R S / ANH SSJ-8 ST R S / ANH SSJ-8A ST R S / TURBO-1 / PCH-2 / PCH-3 / PCH-5 / PCH-6 / PCH-7 / PCH-4 / TUCURA-1 / BONE-1 / EL FARO-1 / JARAGUAY NORTE-1 / JARAGUAY NORTE-2 / JARAGUAY NORTE-3 / JARAGUAY NORTE-4 / JARAGUAY NORTE-5 / PARUMAS-1 / PIRU-1 / SAN RAFAEL-1 / GERMAN-2 (LOBO-1) / GERMAN-3 (LOBO-2) / GERMAN-4 (LOBO-3) / LORICA-1 / LA RADA-1 / SAN SEBASTIAN-2 / SOLEDAD-1 / BOLIVAR SOUTH-4 / BOLIVAR SOUTH-1 / BOLIVAR SOUTH-2 / BOLIVAR SOUTH-3 / BOLIVAR SOUTH-5 / BOLIVAR SOUTH-6 / SANTA SUSANA-1 / BOLIVAR WEST-12 / CLARO-1 / BOLIVAR WEST-13 / COLOMBOY-1 / AGUAS PRIETAS-1 / FLORESANTO-6 / AGUAS PRIETAS-2 / FLORESANTO-7 / ARBOLETES-1X / FLORESANTO-8 / CHINU-1 / FLORESANTO-9 / CHINU-2 / FLORESANTO-10 / CHINU-3 / FLORESANTO-11 / CHINU-5 / RIO NUEVO-1 / CHINU-7 / SAN ANDRES-1 / CORDOBA-1 / SAHAGUN-1 / DELTA-1 / ANH-SSJ-015-STR-S / CARMEN-1 / DELTA-2 / ANH-SSJ-15-SSR-S / CURRAMBA EST-1 / EL DESEO-1 / ANH-SSJ-17-SSR-S / CAMPITO-1 / EL PENON-1 / ANH-SSJ-17-STR-S / TOLU-1 / CAMPITO-2 / FLORESANTO-1 / LIMON-2 / ANH-SSJ-18-SSR-S / TOLU-2 / CAMPITO-3 / FLORESANTO-1G / EL FARO-1 ST / ANH-SSJ-18-STR-S / TOLU-3 / CAMPECHE-1 / FLORESANTO-1V / FLORESANTO-1C / ANH-SSJ-20A-STR-S / NUEVA ERA-1 / BARANOA-1 / FLORESANTO-2 / SAN ANDRES-2 / P-8(2) (DON GABRIEL) / ANH-SSJ-20-SSR-S / CHINU-8 / ARENAL-1 / FLORESANTO-3 / ANH TIERRALTA 2-X-P / P-8(1) (OVEJAS) / ANH-SSJ-20-STR-S / CHINU-9 / ARROYO COCAMBA-1 / FLORESANTO-4 / SAN SEBASTIAN-1 / P-8 / ANH-SAN-ANTERO-1 / PORVENIR-2 / CARACOLI-1 / FLORESANTO-5 / P-14 EL VARAL / ANH-LOS-PAJAROS-1 / LA ESPERANZA-1 / CARMEN-2 / FLORESANTO-12 / ANH-MOAMBO-1 / LA ARENA-1 / CIBARCO-1 / GERMAN-1 / ANH-LA X-1 / ANH-COSTA-AZUL-1 / GALAPA-1 / GUIBERSON-1 / GALAPA-2 / GUIBERSON-2 / GUARUCO-1 / HECHIZO-1 / GUARUCO-2 / JARAGUAY SUR-1 / GUARUCO-3 / LA RISA-1 / LAS PERDICES-1 / LA YE-1 / LAS PERDICES-1A / LIMON-1 / LAS PERDICES-2 / LIMON-1 (LORENCITO) / BUENAVISTA-1 / GEMINIS-15 / LAS PERDICES-3 / LIMON-2 (LORENCITO) / BALSAMO-2 / LAS PERDICES-4 / LA MORA-1 / GUAMO-1 / LAS PERDICES-4A / MORROCOY-1 / MEDIALUNA-1 / LAS PERDICES-5 / REMOLINO-1 / LAS PERDICES-6 / SAN ANDRES A-1 / SALAMANCA-1 / LAS PERDICES-7 / SANTA RITA-1 / LAS PERDICES-8 / SAN SEBASTIAN-3 / LAS PERDICES-9 / SAN SEBASTIAN-3ST / LAS PERDICES-10 / SINU-1 / MANATI-1 / SINU-2 / MOLINERO-1 / SINU-3 / MOLINERO-2 / MOLINERO-3X / PERDICES WEST-1 / POLONUEVO-1 (ARROYO GRANDE-1) (PALONUEVO 105-1) / REPELON-1 / REPELON-2 / REPELON-3 / TUBARA-1 / TUBARA-2 / TUBARA-3 / TUBARA-4 / USIACURI-1 / USIACURI-1A / STRAT GX-1 / USIACURI-1B / STRAT GX-2 / USIACURI-1C / APOLO-1 / CALIPSO-1 / CORDOBA SOUTH-1 / ANH CONUCO-1 / FLORESANTO-2G / ANH JUAN DE ACOSTA-1 / NECOCLI-1 / ANH EL PABILO-1 / PIEDRECITA-1X (1570-1X) / ANH SSJ LAS LAURAS-1X / PORQUERIA-1X (1609-1X) / ANH-SSJ-NUEVA ESPERANZA-1X / ANH-SSJ-LA-ESTRELLA-1X / BULLERENGUE SUR-1 / P-12 ALMAGRA / P-2 CHALAN / P-4A OVEJAS VIA CHALAN / SAMAN EST-1 / TOLU-4 / ANH-SAN CAYETANO-1 / TOLU-5 / ANH-PIEDRA BLANCA-1 / TOLU-6 / ANH-SAN JACINTO-1 / P-10 TORRENTE / BULLERENGUE SUR-3 / P-3 TOLU VIEJO / BETULIA-1",
DescripMetEvConsDom="Método de evaluación de la calidad basado en la inspección del contenido de valores de atributos de metadatos diligenciados pertinentes  respecto al universo del conjunto de datos",
TipEvaluaMet="Directo Externo",
ZonaPais="No definido",
date="39083",
date1="39083",
date2="39083",
dateType="A\u00f1o",
datestamp="39083",
datestamp1="39083",
datestamp2="39083",
description1="No definido",
eastBoundLongitude="-73,94",
northBoundLatitude="11,24",
path="http://srvagspru.sgc.gov.co/oairequest?verb=GetRecord&identifier=BASIN_01_SSJN_SGC&metadataPrefix=oai_dc",
source="",
southBoundLatitude="7,03",
westBoundLongitude="-77,13",

)

def ConvertToJSon( **parametros):
    dic= METADATO_CONSTANTE
    for parametro in parametros:
            dic[parametro]=str((parametros[parametro])).split(";")
    stringJson =json.dumps(dic,separators=(',', ': '),sort_keys=True)
    return stringJson
print "INSERT INTO records (record_id , modified, metadata) VALUES ('BASIN_04_SSJN_SGC',"+ time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+",'"+ConvertToJSon()+"')"
cursor.execute("INSERT INTO records (record_id , modified, metadata) VALUES ('BASIN_04_SSJN_SGC',"+"'"+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+"','"+ConvertToJSon()+"')")
cursor.execute("""INSERT INTO setrefs (record_id , set_id) VALUES ('BASIN_04_SSJN_SGC','geoportal')""")

print "coneccion"
con.commit()
con.close()


