import arcpy, os, sys

GeodatabaseIMSMA=r"C:\Users\fgonzalezf\Documents\APN\IMSMA.gdb"
GeodatabaseSDEImsma=r"C:\Users\fgonzalezf\Documents\APN\Prueba_cargue_IMSMA.gdb"

fcprueba= GeodatabaseIMSMA+ os.sep+ "Hazard_Reductions_polygon"
fcpruebasalida=GeodatabaseSDEImsma+os.sep+"Hazard_Reductions_polygon"
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
        return sorted({row[1] for row in cursor})





def actualizarValores(Featin, FeatOut, fields):
    with arcpy.da.SearchCursor(Featin, fields) as cursor:
    # For each row, evaluate the WELL_YIELD value (index position
    # of 0), and update WELL_CLASS (index position of 1)

        for row in cursor:
            expresion=arcpy.AddFieldDelimiters(GeodatabaseIMSMA,fields[1])
            query= expresion+"='"+row[1]+"'"
            print row[1]
            estado=False
            edit = arcpy.da.Editor (GeodatabaseSDEImsma)
            edit.startEditing ()
            edit.startOperation()
            with arcpy.da.UpdateCursor(FeatOut, fields, query) as cursor2:
                for row2 in cursor2:
                    estado=True
                    print "Actualizando Valores"
                    if row[1]==row2[1]:
                        for i in range(len(row)):
                            row2[i]=row[i]
                    cursor2.updateRow(row2)
            if estado==False:
                print "ingresando valores nuevos"
                cursor3 = arcpy.da.InsertCursor(FeatOut, fields)
                cursor3.insertRow(row)
            edit.stopOperation()
            edit.stopEditing("True")


            # Update the cursor with the updated list


arcpy.env.workspace=GeodatabaseIMSMA
ListaFeatEntrada= arcpy.ListFeatureClasses()
listaF=ListaCampos(fcprueba)
print listaF
actualizarValores(fcprueba,fcpruebasalida,listaF)


