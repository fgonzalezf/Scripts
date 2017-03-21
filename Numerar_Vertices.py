import arcpy,os,sys

arcpy.env.overwriteOutput=True
infc = r"C:\Users\Fernando\Downloads\Nuevo_Shape\area_serv.shp"
outfc=r"C:\Users\Fernando\Downloads\Nuevo_Shape\area_puntos.shp"

arcpy.env.workspace=infc
sr=arcpy.Describe(infc).spatialReference

Letras={1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H",9:"I",10:"J",11:"K",12:"L",12:"M",13:"N",
        14:"O",15:"P",16:"Q",17:"R",18:"S",19:"T",20:"V",21:"W",21:"X",22:"Y",23:"Z",24:"AA",25:"AB",26:"AC"}

arcpy.CreateFeatureclass_management(os.path.dirname(outfc),os.path.basename(outfc),"POINT",infc,"","",sr)

def ListaCampos(Feat):
    ListaFinal=[]
    ListaFinal.append("OID@")
    ListaInit= arcpy.ListFields(Feat)
    for field in ListaInit:
        if field.editable==True and field.type!="Geometry" and field.type!="OID":
            ListaFinal.append(field.name)
    Des= arcpy.Describe(Feat)
    if Des.shapeType=="Point":
        ListaFinal.append('SHAPE@XY')
    else:
        ListaFinal.append('SHAPE@')
    return ListaFinal
fields = ListaCampos(infc)


for row in arcpy.da.SearchCursor(infc,fields):
    print("Feature {}:".format(row[0]))
    partnum = 0
    for part in row[1]:
        print("Part {}:".format(partnum))
        for pnt in part:
            if pnt:
                print("{}, {}".format(pnt.X, pnt.Y))
            else:
                print("Interior Ring:")
        partnum += 1
