import arcpy, os, sys
import arcpy.mapping

class LicenseError(Exception):
    pass


arcpy.env.overwriteOutput=True
puntosCota=arcpy.GetParameterAsText(0)
curvasNivel=arcpy.GetParameterAsText(1)
escala=arcpy.GetParameterAsText(2)

def rango(Escala):
    rango = 0;
    if Escala=="1:1.000":
        rango=1
    elif Escala=="1:2.000":
        rango=2
    elif Escala=="1:5.000":
        rango=5
    elif Escala=="1:10.000":
        rango=10
    elif Escala=="1:25.000":
        rango=25
    elif Escala=="1:50.000":
        rango=50
    elif Escala=="1:100.000":
        rango=100
    return rango

def carpeta (layer):
    desc=arcpy.Describe(layer)
    datasource=desc.featureClass.catalogPath
    Carpeta = ""
    if "." in str(datasource):
        Carpeta = os.path.dirname(datasource.split(".")[0])
    else:
        pass
    return Carpeta

def MapFieldRelObjectID(CurFC):
    '''Mapeo de campos para geometrias'''
    FieldMappings = arcpy.FieldMappings()
    FieldMappings.addTable(CurFC)
    FldMap_InOID = arcpy.FieldMap()
    FldMap_InOID.addInputField(CurFC, 'OBJECTID')
    Fld_InOID = FldMap_InOID.outputField
    Fld_InOID.name = 'IDTEMP'
    FldMap_InOID.outputField = Fld_InOID
    FieldMappings.addFieldMap(FldMap_InOID)

    return FieldMappings

try:
    if arcpy.CheckExtension("3D") == "Available":
        arcpy.CheckOutExtension("3D")
    else:
        # raise a custom exception
        #
        raise LicenseError

    TIN = carpeta(puntosCota)+r"\Tin"
    FACTOR =rango(escala)


    # Extrayendo el Limite de las curvas
    arcpy.CreateTin_3d(TIN,"",[[curvasNivel,"TALT", "masspoints"]],"CONSTRAINED_DELAUNAY")
    #arcpy.AddField_management(puntosCota,"IDTEMP","LONG")

    desc=arcpy.Describe(puntosCota)
    datasource=desc.featureClass.catalogPath
    NombreCota = os.path.basename(datasource)

    campo = arcpy.AddFieldDelimiters(datasource,"OBJECTID")
    arcpy.AddMessage(campo)
    #arcpy.CalculateField_management(puntosCota,"IDTEMP",campo,"VB")
    arcpy.FeatureClassToFeatureClass_conversion(puntosCota,"in_memory","CotaTemp1","",MapFieldRelObjectID(puntosCota))
    arcpy.InterpolateShape_3d(TIN,"in_memory/CotaTemp1","in_memory/CotaTemp")
    arcpy.AddZInformation_3d("in_memory/CotaTemp",'Z')
    arcpy.DeleteField_management("in_memory/CotaTemp","ALTURA_SOBRE_NIVEL_MAR")



    arcpy.AddJoin_management(puntosCota,"OBJECTID","in_memory/CotaTemp","IDTEMP","KEEP_ALL")

    Fields = arcpy.ListFields(puntosCota)

    campoSelect= None
    campoAltura=None
    campoZ=None
    for field in Fields:
        if "Z" in field.name.upper():
            campoZ=field.name
        elif "ALTURA_SOBRE_NIVEL_MAR" in field.name.upper():
            campoAltura=field.name

    CotaId = NombreCota+".OBJECTID"
    arcpy.AddMessage(campoSelect)
    arcpy.AddMessage(campoAltura)
    arcpy.AddMessage(campoZ)

    rows = arcpy.SearchCursor(puntosCota)

    DicObjetID=[]
    DicOjectIdes=[]
    for row in rows:
        try:
            Znub=row.getValue(campoZ)
            Alt=row.getValue(campoAltura)
            Res=((float(Znub)/float(FACTOR))-(float(Znub)//float(FACTOR)))*FACTOR
            arcpy.AddMessage(str(Res))
            IZ= float(Znub)-Res
            DR=IZ+FACTOR
            arcpy.AddMessage("izquieda: "+ str(IZ)+ "   Derecha: "+str(DR)  + "  Factor: "+str(FACTOR)+ "Altura Estimada: "+ str(Znub))
            if Alt>IZ and Alt<DR:
                    pass

            else:
                if Res==0:
                    DicOjectIdes.append(row.getValue(CotaId))
                else:
                    DicObjetID.append(row.getValue(CotaId))

        except Exception as e:
            arcpy.AddMessage(e.message)
    query=""
    query2=""
    if DicObjetID:
        for ob in DicObjetID:
            query=query+str(ob)+","
    if DicOjectIdes:
        for ob in DicOjectIdes:
            query2=query2+str(ob)+","
    query = campo +" in ("+ query[:-1] +")"
    query2 = campo +" in ("+ query2[:-1] +")"
    arcpy.AddMessage(query)
    arcpy.AddMessage(query2)
    arcpy.RemoveJoin_management(puntosCota,"CotaTemp")
    arcpy.Delete_management(TIN)
    try:
        #mxd = arcpy.mapping.MapDocument("CURRENT")
        #df=arcpy.mapping.ListDataFrames(mxd)[0]
        arcpy.AddMessage("bien ")
        if DicObjetID:
            Layer1=arcpy.MakeFeatureLayer_management(puntosCota,"Puntos de Cota Fuera de Rango",query)
            arcpy.SetParameter(3,Layer1)

        if DicOjectIdes:
            Layer2=arcpy.MakeFeatureLayer_management(puntosCota,"Puntos de Cota Para Revisar (Indesicion)",query2)
            arcpy.SetParameter(4,Layer2)
    except Exception as e:
        arcpy.AddMessage("Error: "+ e.message)

except LicenseError:
    arcpy.AddMessage("No hay Licencia 3D Disponible")
except:
    arcpy.AddMessage(arcpy.GetMessages(2))


