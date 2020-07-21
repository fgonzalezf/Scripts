import arcpy, os,sys

#agregar campo lista de feature class
Geodatabase = r"C:\Users\Equipo\Documents\SGC\Amenaza_Sismica\Amenaza_Sismica_2020.gdb"
arcpy.env.workspace=Geodatabase
listaCapas = arcpy.ListFeatureClasses()




expression = "getClass(!gridcode!)"
codeblock = """def getClass(area):
    if area == 1:
        return "0 - 0.005"
    if area == 2:
        return "0.005 - 0.01"
    if area == 3:
        return "0.01 - 0.02"
    if area == 4:
        return "0.02 - 0.03"
    if area == 5:
        return "0.03 - 0.05"
    if area == 6:
        return "0.05 - 0.075"
    if area == 7:
        return "0.075 - 0.1"
    if area == 8:
        return "0.1 - 0.2"
    if area == 9:
        return "0.2 - 0.3"
    if area == 10:
        return "0.3 - 0.5"
    if area == 11:
        return "0.5 - 1"
    if area == 12:
        return "1 - 1.5"
    if area == 13:
        return "1.5 - 2.5"
    if area == 14:
        return "2.5 - 3.5"
    if area == 15:
        return "3.5 - 100" """


for fc in listaCapas:
    campo = fc.split("_")[0]+"_"+fc.split("_")[1]
    try:
        arcpy.AddField_management(fc,campo,"TEXT","","","255")
    except:
        pass

    arcpy.CalculateField_management(fc,campo,expression,"PYTHON_9.3",codeblock)
    print fc


