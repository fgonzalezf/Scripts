import arcpy,os,sys

Entrada=r"D:\APN\hazard.mdb\hazard2"
Salida=r""


desc = arcpy.Describe(Entrada)

print desc.dataType

if desc.dataType=="Table":

