import arcpy, os, sys

GeodatabaseIMSMA=r"D:\APN\IMSMA.gdb"
GeodatabaseSDEImsma=r""

fcprueba= GeodatabaseIMSMA+ os.sep+ "Hazard_Reductions_polygon"
def ListaCampos(Feat):
    ListaFinal=[]
    ListaInit= arcpy.ListFields(Feat)
    for field in ListaInit:
        if field.editable==True and field.type!="Geometry" and field.type!="OID":
            ListaFinal.append(field.name)
    ListaFinal.append('SHAPE@')
    return ListaFinal

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

print ListaCampos(fcprueba)

def IngresarRegistrosNuevos(Feat,row,fields):
    cursor = arcpy.da.InsertCursor(Feat, fields)
    cursor.insertRow(row)

def actualizarValores(Featin, FeatOut, fields):
    with arcpy.da.SearchCursor(Featin, fields) as cursor:
    # For each row, evaluate the WELL_YIELD value (index position
    # of 0), and update WELL_CLASS (index position of 1)
        for row in cursor:
            for i in range(len(row)):
                row[i]
            # Update the cursor with the updated list
            cursor.updateRow(row)

arcpy.env.workspace=GeodatabaseIMSMA
ListaFeatEntrada= arcpy.ListFeatureClasses()
