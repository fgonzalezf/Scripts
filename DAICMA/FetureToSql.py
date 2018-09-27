#Requires: Esri's ArcPy.da module and PyODBC module
#Note: Search for <VARIABLE> to replace with new values, and update inputs

import arcpy, pyodbc

def fn_ReadPolygons(fc_in,wkid):
    #This function loops through a polygon layer and converts geometry to WKT format
    #Additional attributes can also be added for insert
    #The input layer and WKID of the Geography type is required
    for row in arcpy.da.SearchCursor(fc_in, ["SHAPE@WKT"]):
        sqlInsertStatement = "INSERT INTO SpatialTable (GeogCol1) VALUES (geography::STMPolyFromText("
        sqlInsertStatement += "'" + row[0] + "'," + wkid + "))"
        fn_SqlStatement(sqlInsertStatement, "Load Polygon Statement")
#End function - fn_ReadPolygons

def fn_SqlStatement(sqlStatement, sqlPurpose):
    #This function connects to SQL Server and runs the SQL commands
    #The full SQL Statement is passed to the function, along with a brief description for error checking
    try:
        cnxn_SQL = pyodbc.connect("DRIVER={SQL Server};SERVER=<VARIABLE>;DATABASE=<VARIABLE>;UID=<VARIABLE>;PWD=<VARIABLE>")
        cursor_SQL = cnxn_SQL.cursor()
        cursor_SQL.execute(sqlStatement)
        cnxn_SQL.commit()
        cnxn_SQL.close()
    except:
        print 'error in fn_SqlStatement: ' + sqlPurpose
#End function - fn_SqlStatement

