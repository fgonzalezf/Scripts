import arcpy, os, sys

FeatEntrada= r"D:\Proyecto\fernando.gonzalez\Fernando\enviar_igac\enviar21.mdb\Datos_Extraidos"



tabla=arcpy.CreateTable_management ("in_memory", "tabla")

#Campos

fields =["ACTION_CODE","POI_PVID","PS3_BLEND_POI_ID","FACILITY_CODE","POI_NAME_LANG_CODE","POI_NAME","POI_ADDRESS_LANG_CODE","ADDRESS_NUMBER","COUNTRY","LATITUDE","LONGITUDE","PHONE_NUMBER","CHAIN_ID","CUISINE_ID","BUILDING_TYPE","SUPPLIER_POI_ID","STREET_BASE_NAME","POSTAL_CODE","PROTECTED_ID","CALL_REVIEW_DATE","SOURCE_CODE","NUMBER","STREET_SIDE"]

for field in fields:
    arcpy.AddField_management("in_memory/tabla", field, "TEXT", "", "", "250")


tablaFeat=arcpy.TableToTable_conversion(FeatEntrada, "in_memory", "feat")

def Mapa(fieldmappings,FeatEntrada, CampoEntrada , CampoSalida):
        fieldmap = fieldmappings.getFieldMap(fieldmappings.findFieldMapIndex(CampoSalida))
        fieldmap.addInputField(FeatEntrada, CampoEntrada)
        fieldmappings.replaceFieldMap(fieldmappings.findFieldMapIndex(CampoSalida), fieldmap)
        fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(CampoEntrada))
        return fieldmappings

fieldmapping = arcpy.FieldMappings()
fieldmapping.addTable("in_memory/tabla")
fieldmapping.addTable("in_memory/feat")
fieldList = arcpy.ListFields("in_memory/tabla")
for field in fieldList:
        if field.name=="TIPO_INCONCISTENCIA":
            fieldmapping= Mapa(fieldmapping,featIn, "TIPO_INCONCISTENCIA" ,  "TIPO_INCONSISTENCIA")
        elif field.name=="CAPA_INCONCISTENCIA":
            fieldmapping= Mapa(fieldmapping,featIn, "CAPA_INCONCISTENCIA" ,  "CAPA_INCONSISTENCIA")
arcpy.Append_management(featIn, featOut, "NO_TEST",fieldmapping)
arcpy.TableToTable_conversion("in_memory/tabla", r"D:\Proyecto\fernando.gonzalez\Fernando\enviar_igac\enviar21.mdb", "prueba")
