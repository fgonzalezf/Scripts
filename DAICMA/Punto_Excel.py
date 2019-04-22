import arcpy, os, sys
GDB=r'C:\Users\APN\Documents\APN\GDB\GUA_PTR.mdb'
arcpy.CreateFeatureclass_management(GDB,"Puntos","POINT")

Capa= GDB+ os.sep+ "Puntos"

arcpy.AddField_management(Capa,"DIA","SHORT","","","","DIA")
arcpy.AddField_management(Capa,"MES","SHORT","","","","MES")
arcpy.AddField_management(Capa,"ANIO","SHORT","","","","ANIO")
arcpy.AddField_management(Capa,"HORA","SHORT","","","","HORA")
arcpy.AddField_management(Capa,"DIVISION","TEXT","","","500","DIA")
arcpy.AddField_management(Capa,"FT","TEXT","","","500","FT")
arcpy.AddField_management(Capa,"BRIGADA","TEXT","","","500","BRIGADA")
arcpy.AddField_management(Capa,"UNIDAD","TEXT","","","500","UNIDAD")
arcpy.AddField_management(Capa,"DEPARTAMENTO","TEXT","","","500","DEPARTAMENTO")
arcpy.AddField_management(Capa,"MUNICIPIO","TEXT","","","500","MUNICIPIO")
arcpy.AddField_management(Capa,"VEREDA","TEXT","","","500","VEREDA")
arcpy.AddField_management(Capa,"CANTIDAD","SHORT","","","","CANTIDAD")
arcpy.AddField_management(Capa,"TIPO_ARTEFACTO","TEXT","","","500","TIPO_ARTEFACTO")
arcpy.AddField_management(Capa,"GRADO","TEXT","","","500","GRADO")
arcpy.AddField_management(Capa,"NOMBRES","TEXT","","","500","NOMBRES")
arcpy.AddField_management(Capa,"APELLIDOS","TEXT","","","500","APELLIDOS")
arcpy.AddField_management(Capa,"CEDULA","LONG","","","","CEDULA")
arcpy.AddField_management(Capa,"RESUMEN_HECHOS","TEXT","","","4000","RESUMEN_HECHOS")
arcpy.AddField_management(Capa,"GRUPO_ARMADO","TEXT","","","500","GRUPO_ARMADO")
arcpy.AddField_management(Capa,"FRENTE_COMISION","TEXT","","","500","FRENTE_COMISION")
arcpy.AddField_management(Capa,"LATITUD","DOUBLE","","","","LATITUD")
arcpy.AddField_management(Capa,"LONGITUD","DOUBLE","","","","LONGITUD")