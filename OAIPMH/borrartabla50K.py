import arcpy,sys

tabla =sys.argv[1]
tamanoTabla=4251499
ciclos =tamanoTabla/50000

for x in xrange(0,ciclos):
    tableview=arcpy.MakeTableView_management(tabla,"tableView","ObjectID<"+str(x*50000))
    arcpy.DeleteRows_management("tableView")
    arcpy.AddMessage("ObjectID<"+str(x*50000)+"...."+str(x)+ " de "+ str(ciclos))
    arcpy.Delete_management("tableView")