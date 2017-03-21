__author__ = 'fgonzalezf'
import json
import urllib2
import arcpy,os

GeodatabaseEntrada= r"D:\SGC\Estaciones.mdb"
Feat=GeodatabaseEntrada+ os.sep + "Estaciones"
arcpy.env.overwriteOutput = True
sr =arcpy.CreateSpatialReference_management("4326")
arcpy.CreateFeatureclass_management(GeodatabaseEntrada,"Estaciones","POINT","","","",sr)
url="http://bdrsnc.sgc.gov.co/sismologia1/service_web/capa_estaciones.php"
response = urllib2.urlopen(url)
fields=[]

Ctl=False
for line in response:
    if "[{" in line:
        data = json.loads(line)
for dat in data:
    if Ctl==False:
                fields=dat.keys()
                for field in fields:
                    if field=="LATITUD" or field=="LONGITUD" or field=="ALTITUD":
                        arcpy.AddField_management(Feat,field,"DOUBLE")
                    elif field=="RED_MONITOREO" or field=="ID" or field=="ALTITUD":
                        arcpy.AddField_management(Feat,field,"SHORT")
                    elif field=="FECHA_RETIRO" or field=="FECHA_INSTALACION":
                        arcpy.AddField_management(Feat,field,"DATE")
                    else:
                        arcpy.AddField_management(Feat,field,"TEXT","","","100")

    Ctl=True
fields.append("SHAPE@XY")
cursor = arcpy.da.InsertCursor(Feat,fields)
for dato in data:
    print dato
    row=[]
    for key,value in dato.items():
        if key=="LATITUD" or key=="LONGITUD" or key=="ALTITUD":
            row.append(float(value))
        elif key=="RED_MONITOREO" or key=="ID" or key=="ALTITUD":
            row.append(int(value))
        elif key=="FECHA_RETIRO" or key=="FECHA_INSTALACION":
            pass
            row.append(value)
        else:
            row.append(str(value))
    cords=(float(dato["LONGITUD"]),float(dato["LATITUD"]))
    row.append(cords)
    cursor.insertRow(row)






