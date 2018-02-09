import arcpy, os,sys

arcpy.env.workspace=r""


mxd = arcpy.mapping.MapDocument(r"C:\Project\Project.mxd")
mxd.findAndReplaceWorkspacePaths(r"C:\Project\Data", r"C:\Project\Data2")
mxd.saveACopy(r"C:\Project\Project2.mxd")
del mxd