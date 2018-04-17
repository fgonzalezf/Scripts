#-*- coding: utf-8 -*-
import arcpy, os, sys

arcpy.env.workspace = r'C:\Users\APN\Documents\SGC\Sismos\nuevo.gdb'

in_file = 'TablaSismos'
out_file = 'TablaSismosModificada2'

# Create the necessary FieldMap and FieldMappings objects
fmFecha = arcpy.FieldMap()
fmRegion = arcpy.FieldMap()
fmEstado = arcpy.FieldMap()
fmLongitud = arcpy.FieldMap()
fmLatitud = arcpy.FieldMap()
fmProfundidad = arcpy.FieldMap()
fmMagnitud = arcpy.FieldMap()
fmMunicipios = arcpy.FieldMap()
fms = arcpy.FieldMappings()

# Each field with accident data begins with 'Yr' (from Yr2007 to Yr2012).
# The next step loops through each of the fields beginning with 'Yr',
# and adds them to the FieldMap Object
for field in arcpy.ListFields(in_file):
    if field.name =="FECHA" or field.name =="FECHAUTC":
        fmFecha.addInputField(in_file, field.name)

# Set the merge rule to find the mean value of all fields in the
# FieldMap object
fmFecha.mergeRule = 'Join'

# Set properties of the output name.
f_name = fmFecha.outputField
f_name.name = 'Tiempo_de_origen'
f_name.aliasName = 'Tiempo de origen'
fmFecha.outputField = f_name

# Add the intersection field to the second FieldMap object
fmRegion.addInputField(in_file, "DESCRIPCION")
f_name = fmRegion.outputField
f_name.name = 'Region'
f_name.aliasName = 'Región'
fmRegion.outputField = f_name

fmRegion.addInputField(in_file, "ESTADO")
f_name = fmRegion.outputField
f_name.name = 'Estado'
f_name.aliasName = 'Estado'
fmEstado.outputField = f_name

fmLatitud.addInputField(in_file, "LATITUD")
f_name = fmLatitud.outputField
f_name.name = 'Latitud'
f_name.aliasName = 'Latitud'
fmLatitud.outputField = f_name

fmLongitud.addInputField(in_file, "LONGITUD")
f_name = fmLongitud.outputField
f_name.name = 'Longitud'
f_name.aliasName = 'Longitud'
fmLongitud.outputField = f_name

fmMunicipios.addInputField(in_file, "LOCALIZACION")
f_name = fmMunicipios.outputField
f_name.name = 'Municipios_Cercanos'
f_name.aliasName = 'Municipios Cercanos'
fmMunicipios.outputField = f_name

fmProfundidad.addInputField(in_file, "PROFUNDIDAD")
f_name = fmProfundidad.outputField
f_name.name = 'Profundidad'
f_name.aliasName = 'Profundidad'
fmProfundidad.outputField = f_name

fmMagnitud.addInputField(in_file, "MAGNITUD")
f_name = fmMagnitud.outputField
f_name.name = 'Magnitud'
f_name.aliasName = 'Magnitud'
fmMagnitud.outputField = f_name


# Add both FieldMaps to the FieldMappings Object

fms.addFieldMap(fmRegion)
fms.addFieldMap(fmFecha)
fms.addFieldMap(fmEstado)

fms.addFieldMap(fmLongitud)
fms.addFieldMap(fmLatitud)
fms.addFieldMap(fmMunicipios)
fms.addFieldMap(fmProfundidad)
fms.addFieldMap(fmMagnitud)

# Create the output feature class, using the FieldMappings object
arcpy.TableToTable_conversion(in_file, "in_memory", out_file, field_mapping=fms)