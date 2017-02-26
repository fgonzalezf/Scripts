import arcpy, os, sys

FeatEntrada =sys.argv[1]
FeatPlanchas =sys.argv[2]

arcpy.env.workspace=FeatEntrada
try:
    arcpy.AddField_management(FeatEntrada,"Xmin","DOUBLE")
    arcpy.AddField_management(FeatEntrada,"Xmax","DOUBLE")
    arcpy.AddField_management(FeatEntrada,"Ymin","DOUBLE")
    arcpy.AddField_management(FeatEntrada,"Ymax","DOUBLE")
except:
    pass

with arcpy.da.UpdateCursor(FeatEntrada, ['PLANCHA','Xmin','Xmax','Ymin','Ymax']) as cursor:

    for row in cursor:
        exptemp="'"+str(row[0]).replace(",","','")+"'"
        print exptemp
        expression = "PLANCHA IN ("+exptemp+")"
        with arcpy.da.SearchCursor(FeatPlanchas, ['PLANCHA','Xmin','Xmax','Ymin','Ymax'],where_clause=expression) as cursorp:
            xmin=180
            xmax=-180
            ymin=90
            ymax=-90
            for rowp in cursorp:
                if rowp[1]<xmin:
                    xmin=rowp[1]
                if rowp[2]>xmax:
                    xmax=rowp[2]
                if rowp[3]<ymin:
                    ymin=rowp[3]
                if rowp[4]>ymax:
                    ymax=rowp[4]
        row[1] = xmin
        row[2] = xmax
        row[3] = ymin
        row[4] = ymax
        cursor.updateRow(row)




