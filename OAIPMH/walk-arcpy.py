
import arcpy,os
workspace=r"C:\temp\EPISODAPROD.sde"
for dirpath, dirnames, filenames in arcpy.da.Walk(workspace,datatype=['Any']):

    print dirpath
