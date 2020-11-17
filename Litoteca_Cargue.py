#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
# Author:      fgonzalezf
# Created:     23/02/2015
# Copyright:   (c) fgonzalezf 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, os, sys
carpeta=sys.argv[1]
archivoExcel=sys.argv[2]
origen=sys.argv[3]
cargueSDE=sys.argv[4]
#carpeta = r"C:\Users\fgonzalezf\Documents\Hoja_Vida_2015\prueba2"
#archivoExcel = r"C:\Users\fgonzalezf\Documents\Hoja_Vida_2015\Litoteca_Completo_marzo16.xlsx"
#origen = "Colombia Bogota Zone"
#cargueSDE = "false"

def Mapa(fieldmappings, FeatEntrada, CampoSalida, CampoEntrada):
        fieldmap = fieldmappings.getFieldMap(fieldmappings.findFieldMapIndex(CampoSalida))
        fieldmap.addInputField(FeatEntrada, CampoEntrada)
        fieldmappings.replaceFieldMap(fieldmappings.findFieldMapIndex(CampoSalida), fieldmap)
        fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(CampoEntrada))
        return fieldmappings

def validarMuestra(tabla):
    arcpy.CreateTable_management (os.path.dirname(tabla), "MuestraVal")
    tabla2 = os.path.dirname(tabla) + os.sep + "MuestraVal"
    fields = arcpy.ListFields(tabla)
    try:
        for field in fields:
            if field.name == "Coordenada_Este__m_" or field.name == "Coordenada_Norte__m_"or field.name == "Latitud" or field.name == "Longitud":
                arcpy.AddField_management(tabla2, field.name, "DOUBLE")
            elif field.name == "Fecha_Muestra":
                arcpy.AddField_management(tabla2, field.name, "DATE")
            elif  field.name == "Tipo_Código":
                arcpy.AddField_management(tabla2, field.name, "TEXT", "", "", 30)
            elif field.name == "OBJECTID":
                pass
            else:
                arcpy.AddField_management(tabla2, field.name, "TEXT", "", "", 50)
    except Exception as ex:
            print(ex.message + "  " + "error")

    rowsIn = arcpy.InsertCursor(tabla2)
    fields = arcpy.ListFields(tabla2)
    cursor = arcpy.SearchCursor(tabla)
    for row in cursor:
        rowIn = rowsIn.newRow()
        try:
            for field in fields:
                if field.name == "OBJECTID":
                    pass
                else:
                    if row.getValue(field.name) == '':
                        rowIn.setValue(field.name, None)
                    else:
                        if field.type == "String":
                            rowIn.setValue(field.name, str(row.getValue(field.name))[:field.length])
                        else:
                            rowIn.setValue(field.name, row.getValue(field.name))
            rowsIn.insertRow(rowIn)
        except Exception as ex:
            arcpy.AddMessage(ex.message + "  " + "valores no validos")
    del cursor
    del row
    del rowsIn
    Nombretabla = os.path.basename(tabla)
    arcpy.Delete_management(tabla)
    arcpy.Rename_management(tabla2, Nombretabla)

def validarNucleo(tabla):
    arcpy.CreateTable_management (os.path.dirname(tabla), "NucleoVal")
    tabla2 = os.path.dirname(tabla) + os.sep + "NucleoVal"
    fields = arcpy.ListFields(tabla)
    try:
        for field in fields:
            if field.name == "Coordenada_Este__m_" or field.name == "Coordenada_Norte__m_"or field.name == "Latitud" or field.name == "Longitud":
                arcpy.AddField_management(tabla2, field.name, "DOUBLE")
            elif field.name == "Porcentaje_Recuperación":
                arcpy.AddField_management(tabla2, field.name, "LONG")
            elif field.name == "Localización_Geográfica":
                arcpy.AddField_management(tabla2, field.name, "TEXT", "", "", 80)
            elif field.name == "OBJECTID":
                pass
            else:
                arcpy.AddField_management(tabla2, field.name, "TEXT", "", "", 50)
    except Exception as ex:
            print(ex.message + "  " + "error")
            pass

    rowsIn = arcpy.InsertCursor(tabla2)
    fields = arcpy.ListFields(tabla2)
    cursor = arcpy.SearchCursor(tabla)
    for row in cursor:
        rowIn = rowsIn.newRow()
        try:
            for field in fields:
                if field.name == "OBJECTID":
                    pass
                else:
                    if row.getValue(field.name) == '':
                        rowIn.setValue(field.name, None)
                    else:
                        if field.type == "String":
                            rowIn.setValue(field.name, str(row.getValue(field.name))[:field.length])
                        else:
                            rowIn.setValue(field.name, row.getValue(field.name))
            rowsIn.insertRow(rowIn)
        except Exception as ex:
            arcpy.AddMessage(ex.message + "  " + "valores no validos")
    del cursor
    del row
    del rowsIn
    Nombretabla = os.path.basename(tabla)
    arcpy.Delete_management(tabla)
    arcpy.Rename_management(tabla2, Nombretabla)

def validarSolicitud(tabla):
    arcpy.CreateTable_management (os.path.dirname(tabla), "SolicitudVal")
    tabla2 = os.path.dirname(tabla) + os.sep + "SolicitudVal"
    fields = arcpy.ListFields(tabla)
    try:
        for field in fields:
            if field.name == "Fecha_Autorización_Entrega":
                arcpy.AddField_management(tabla2, field.name, "DATE")
            elif field.name == "Nombre_del_Proyecto":
                arcpy.AddField_management(tabla2, field.name, "TEXT", "", "", 200)
            elif field.name == "OBJECTID":
                pass
            else:
                arcpy.AddField_management(tabla2, field.name, "TEXT", "", "", 50)
    except Exception as ex:
            print(ex.message + "  " + "error")

    rowsIn = arcpy.InsertCursor(tabla2)
    fields = arcpy.ListFields(tabla2)
    cursor = arcpy.SearchCursor(tabla)
    for row in cursor:
        rowIn = rowsIn.newRow()
        try:
            for field in fields:
                if field.name == "OBJECTID":
                    pass
                elif field.name=="Id_Solicitud":
                    rowIn.setValue(field.name, "")
                else:
                    if row.getValue(field.name) == '':
                        rowIn.setValue(field.name, None)
                    else:
                        if field.type == "String":
                            rowIn.setValue(field.name, str(row.getValue(field.name))[:field.length])
                        else:
                            rowIn.setValue(field.name, row.getValue(field.name))
            rowsIn.insertRow(rowIn)
        except Exception as ex:
            arcpy.AddMessage(ex.message + "  " + "valores no validos")
    del cursor
    del row
    del rowsIn
    Nombretabla = os.path.basename(tabla)
    arcpy.Delete_management(tabla)
    arcpy.Rename_management(tabla2, Nombretabla)

spRef = arcpy.SpatialReference(origen)
spMagna = arcpy.SpatialReference("MAGNA")


geodatabase = carpeta + os.sep + "Litoteca.gdb"
geodatabaseSDE = "Database Connections\Litoteca_Edicion.sde"

arcpy.AddMessage(unicode("...Creando Conexión a La tematica Litoteca"))

try:
    arcpy.CreateDatabaseConnection_management("Database Connections",
                                          "Litoteca_Edicion.sde",
                                          "ORACLE",
                                          "sde:oracle11g:sigprod_oda",
                                          "DATABASE_AUTH",
                                          "MLIT",
                                          "MLIT",
                                          "SAVE_USERNAME")
except:
    geodatabaseSDE = "Database Connections\Litoteca_Edicion.sde"
    arcpy.AddMessage("La conexión ya existe")

arcpy.AddMessage("...Exportando XML de la Tematica")
try:
    in_data = geodatabaseSDE
    out_file = carpeta + os.sep + "litoteca.xml"
    export_option = "SCHEMA_ONLY"
    storage_type = "BINARY"
    export_metadata = "METADATA"

    # Execute ExportXMLWorkspaceDocument
    arcpy.ExportXMLWorkspaceDocument_management(in_data, out_file, export_option, storage_type, export_metadata)
except:
    arcpy.AddMessage("...Error exportando Geodatabase")

arcpy.AddMessage("...Importando XML de la Tematica")
try:
    if arcpy.Exists(geodatabase):
        arcpy.Delete_management(geodatabase)
    arcpy.CreateFileGDB_management(carpeta, "Litoteca.gdb")

    target_gdb = geodatabase
    in_file = carpeta + os.sep + "litoteca.xml"
    import_type = "SCHEMA_ONLY"
    config_keyword = "DEFAULTS"

    # Execute ImportXMLWorkspaceDocument
    arcpy.ImportXMLWorkspaceDocument_management(target_gdb, in_file, import_type, config_keyword)
    arcpy.env.workspace = geodatabase
except:
    arcpy.AddMessage("...Error creando geodatabase")

arcpy.AddMessage("...Exportando Tabla de Excel ")
try:
    arcpy.ExcelToTable_conversion(archivoExcel, geodatabase + os.sep + "Solicitud", "Solicitud")
    validarSolicitud(geodatabase + os.sep + "Solicitud")
except:
    arcpy.AddMessage("...Error exportando Solicitud")
try:
    arcpy.ExcelToTable_conversion(archivoExcel, geodatabase + os.sep + "Muestra", "Muestra")
    validarMuestra(geodatabase + os.sep + "Muestra")
except:
    arcpy.AddMessage("...Error exportando Muestra")
try:   
    arcpy.ExcelToTable_conversion(archivoExcel, geodatabase + os.sep + "Nucleo", "Nucleo")
    validarNucleo(geodatabase + os.sep + "Nucleo")
except:
    arcpy.AddMessage("...Error exportando Nucleo")

arcpy.AddMessage("...Creando Fetuare Class De Puntos ")

consulta = "(Coordenada_Este__m_ IS  NULL AND Coordenada_Norte__m_  IS NULL) OR (Latitud  IS NULL AND Longitud IS NULL ) AND (Coordenada_Este__m_>2000000 OR Coordenada_Este__m_<0) OR (Coordenada_Norte__m_>2000000 OR Coordenada_Norte__m_<0)"

if origen != "MAGNA" and origen != "BOGOTA":
        if origen == "Colombia Bogota Zone" or origen == "Colombia E Central Zone"  or origen == "Colombia East Zone" or origen == "Colombia West West Zone"or origen == "Colombia West Zone":
            try:
                layer1 = arcpy.MakeXYEventLayer_management(geodatabase + os.sep + "Muestra", "Coordenada_Este__m_", "Coordenada_Norte__m_", "LayerMuestra", spRef)
                arcpy.CopyFeatures_management("LayerMuestra", geodatabase + os.sep + "Muestra_BOGOTA")
                arcpy.Project_management(geodatabase + os.sep + "Muestra_BOGOTA", geodatabase + os.sep + "Muestra_MAGNA", spMagna, "Bogota_To_MAGNA_Region_8_MB")
                layer3 = arcpy.MakeFeatureLayer_management(geodatabase + os.sep + "Muestra_MAGNA", "Muestra_Layer", consulta)
                arcpy.DeleteFeatures_management("Muestra_Layer")
            except Exception as e:
                arcpy.AddMessage("Error Creando Layer de Puntos: " + e.message)
            try:
                layer2 = arcpy.MakeXYEventLayer_management(geodatabase + os.sep + "Nucleo", "Coordenada_Este__m_", "Coordenada_Norte__m_", "LayerNucleo", spRef)
                arcpy.CopyFeatures_management("LayerNucleo", geodatabase + os.sep + "Nucleo_BOGOTA")
                arcpy.Project_management(geodatabase + os.sep + "Nucleo_BOGOTA", geodatabase + os.sep + "Nucleo_MAGNA", spMagna, "Bogota_To_MAGNA_Region_8_MB")
                layer4 = arcpy.MakeFeatureLayer_management(geodatabase + os.sep + "Nucleo_MAGNA", "Nucleo_Layer", consulta)
                arcpy.DeleteFeatures_management("Nucleo_Layer")
            except Exception as e:
                arcpy.AddMessage("Error Creando Layer de Puntos: " + e.message)
        else:
            try:
                layer1 = arcpy.MakeXYEventLayer_management(geodatabase + os.sep + "Muestra", "Coordenada_Este__m_", "Coordenada_Norte__m_", "LayerMuestra", spRef)
                arcpy.CopyFeatures_management("LayerMuestra", geodatabase + os.sep + "Muestra_BOGOTA")
                arcpy.Project_management(geodatabase + os.sep + "Muestra_BOGOTA", geodatabase + os.sep + "Muestra_MAGNA", spMagna)
                layer3 = arcpy.MakeFeatureLayer_management(geodatabase + os.sep + "Muestra_MAGNA", "Muestra_Layer", consulta)
                arcpy.DeleteFeatures_management("Muestra_Layer")
            except Exception as e:
                arcpy.AddMessage("Error Creando Layer de Puntos: " + e.message)
            try:
                layer2 = arcpy.MakeXYEventLayer_management(geodatabase + os.sep + "Nucleo", "Coordenada_Este__m_", "Coordenada_Norte__m_", "LayerNucleo", spRef)
                arcpy.CopyFeatures_management("LayerNucleo", geodatabase + os.sep + "Nucleo_BOGOTA")
                arcpy.Project_management(geodatabase + os.sep + "Nucleo_BOGOTA", geodatabase + os.sep + "Nucleo_MAGNA", spMagna)
                layer4 = arcpy.MakeFeatureLayer_management(geodatabase + os.sep + "Nucleo_MAGNA", "Nucleo_Layer",)
                arcpy.DeleteFeatures_management("Nucleo_Layer")
            except Exception as e: 
                arcpy.AddMessage("Error Creando Layer de Puntos: " + e.message)
else:
        try:
            layer1 = arcpy.MakeXYEventLayer_management(geodatabase + os.sep + "Muestra", "Latitud", "Longitud", "LayerMuestra", spRef)
            arcpy.CopyFeatures_management("LayerMuestra", geodatabase + os.sep + "Muestra_BOGOTA")
        except Exception as e:
            arcpy.AddMessage("Error Creando Layer de Puntos: " + e.message)
        try:
            layer2 = arcpy.MakeXYEventLayer_management(geodatabase + os.sep + "Nucleo", "Latitud", "Longitud", "LayerNucleo", spRef)
            arcpy.CopyFeatures_management("LayerNucleo", geodatabase + os.sep + "Nucleo_BOGOTA")
        except Exception as e:
            arcpy.AddMessage("Error Creando Layer de Puntos: " + e.message)

        if origen == "BOGOTA":
            try:
                arcpy.Project_management(geodatabase + os.sep + "Muestra_BOGOTA", geodatabase + os.sep + "Muestra_MAGNA", spMagna, "Bogota_To_MAGNA_Region_8_MB")
                layer3 = arcpy.MakeFeatureLayer_management(geodatabase + os.sep + "Muestra_MAGNA", "Muestra_Layer", consulta)
                arcpy.DeleteFeatures_management("Muestra_Layer")
            except Exception as e:
                arcpy.AddMessage("Error Creando Layer de Puntos: " + e.message)
            try:
                arcpy.Project_management(geodatabase + os.sep + "Nucleo_BOGOTA", geodatabase + os.sep + "Nucleo_MAGNA", spMagna, "Bogota_To_MAGNA_Region_8_MB")
                layer4 = arcpy.MakeFeatureLayer_management(geodatabase + os.sep + "Nucleo_MAGNA", "Nucleo_Layer", consulta)
                arcpy.DeleteFeatures_management("Nucleo_Layer")
            except Exception as e:
                arcpy.AddMessage("Error Creando Layer de Puntos: " + e.message)
        else:
            try:
                arcpy.Project_management(geodatabase + os.sep + "Nucleo_BOGOTA", geodatabase + os.sep + "Nucleo_MAGNA", spMagna)
                layer3 = arcpy.MakeFeatureLayer_management(geodatabase + os.sep + "Muestra_MAGNA", "Muestra_Layer", consulta)
                arcpy.DeleteFeatures_management("Muestra_Layer")
            except Exception as e:
                arcpy.AddMessage("Error Creando Layer de Puntos: " + e.message)
            try:
                arcpy.Project_management(geodatabase + os.sep + "Muestra_BOGOTA", geodatabase + os.sep + "Muestra_MAGNA", spMagna)
                layer4 = arcpy.MakeFeatureLayer_management(geodatabase + os.sep + "Nucleo_MAGNA", "Nucleo_Layer", consulta)
                arcpy.DeleteFeatures_management("Nucleo_Layer")
            except Exception as e:
                arcpy.AddMessage("Error Creando Layer de Puntos: " + e.message)

expression1 = "shiftXCoordinate(!SHAPE!)"
codeblock1 = """def shiftXCoordinate(shape):
   point = shape.getPart(0)
   return point.Y"""
expression2 = "shiftXCoordinate(!SHAPE!)"
codeblock2 = """def shiftXCoordinate(shape):
   point = shape.getPart(0)
   return point.X"""
expression3 = "DominioTipoCodigo( !Tipo_Código!)"
codeblock3 = """def DominioTipoCodigo(campo):
  valor=None
  if campo=="Código IGM":
      valor="IGM"
  elif campo=="Código IMN":
      valor="IMN"
  elif campo=="Otro Código":
      valor="OTRO"
  else:
      valor=None
  return valor"""
expression4 = "DominioTipoCodigo(!Origen_de_Gauss! )"
codeblock4 = """def DominioOrigen(campo):
  valor=None
  if campo=="Origen Central":
      valor="OC"
  elif campo=="Origen Este":
      valor="E"
  elif campo=="Origen Este Este":
      valor="EE"
  elif campo=="Origen Oeste":
      valor="W"
  elif campo=="Origen Insular":
      valor="WW"
  else:
      valor=None
  return valor"""
expression5 = "DominioTipoAnalisis(!Tipo_Análisis_Muestra!)"
codeblock5 = """def DominioTipoAnalisis(campo):
  valor=None
  if campo=="Petrografía":
      valor="PTR"
  elif campo=="Mineralogía":
      valor="MNR"
  elif campo=="Geoquímica":
      valor="GQM"
  else:
      valor=None
  return valor"""
expression6 = "DominioTipoAnalisisNucleo(!TIipo_Análisis!)"
codeblock6 = """def DominioTipoAnalisisNucleo(campo):
  valor=None
  if campo=="Análisis Básicos (humedad, cenizas, material volátil)":
      valor="ANAL_BAS"
  elif campo=="Análisis Químicos (fluorescencia de rayos X, difractometría)":
      valor="ANAL_QUIM"
  elif campo=="Análisis Petrográficos (Secciones delgadas, difracción Rayos X, microscopía electrónica SEM)":
      valor="ANAL_PET"
  elif campo=="Registros eléctricos (Gamma Ray, SP -Potencial Espontáneo, Resistividad, Neutrón, Densidad)":
      valor="ANAL_REG"
  else:
      valor=None
  return valor"""
expression7 = "TipoSolicitud(!Tipo_de_Muestra!)"
codeblock7 = """def TipoSolicitud(campo):
  valor=None
  if campo=="Muestra Roca":
      valor="MR"
  elif campo=="Muestra Sedimentos":
      valor="MS"
  elif campo=="Muestra Paleontológica":
      valor="MP"
  elif campo=="Muestra Testigo Perforación":
      valor="MT"
  elif campo=="Núcleo de Perforación":
      valor="NP"
  elif campo=="Rodados":
      valor="R"
  elif campo=="Concentrados de Batea":
      valor="CB"
  elif campo=="Otros":
      valor="OTROS"
  else:
      valor=None
  return valor"""

expression8 = "TipoSolicitud(!Fecha_Muestra!)"
codeblock8 = """def TipoSolicitud(campo):
  valor=""
  if campo=='':
      valor=None
  return valor"""

arcpy.AddMessage("...Calculando valores de Dominios ")
try:
    arcpy.CalculateField_management(geodatabase + os.sep + "Muestra_MAGNA", "Tipo_Código", expression3, "PYTHON", codeblock3)
    arcpy.CalculateField_management(geodatabase + os.sep + "Muestra_MAGNA", "Origen_de_Gauss", expression4, "PYTHON", codeblock4)
    arcpy.CalculateField_management(geodatabase + os.sep + "Muestra_MAGNA", "Tipo_Análisis_Muestra", expression5, "PYTHON", codeblock5)
    arcpy.CalculateField_management(geodatabase + os.sep + "Muestra_MAGNA", "Fecha_Muestra", expression8, "PYTHON", codeblock8)
    arcpy.CalculateField_management(geodatabase + os.sep + "Muestra_MAGNA", "Latitud", expression1, "PYTHON", codeblock1)
    arcpy.CalculateField_management(geodatabase + os.sep + "Muestra_MAGNA", "Longitud", expression2, "PYTHON", codeblock2)

except Exception as e:
    arcpy.AddMessage("Error Calculando Dominios Muestra: " + e.message)

try:
    arcpy.CalculateField_management(geodatabase + os.sep + "Nucleo_MAGNA", "TIipo_Análisis", expression6, "PYTHON", codeblock6)
except Exception as e:
    arcpy.AddMessage("Error Calculando Tipo Analisis Nucleo: " + e.message)

try:
    arcpy.CalculateField_management(geodatabase + os.sep + "Solicitud", "Tipo_de_Muestra", expression7, "PYTHON", codeblock7)
except Exception as e:
    arcpy.AddMessage("Error Calculando Tipo Muestra solicitud: " + e.message)

arcpy.AddMessage("...Cargando Puntos al Modelo Definitivo ")

#### Cargue Solicitud
##
in_put = geodatabase + os.sep + "Solicitud"
output = geodatabase + os.sep + "F33SOL_SOLICITUD"
arcpy.AddMessage(in_put)
arcpy.AddMessage(output)
try:
    if arcpy.Exists(in_put):
        fieldmapping = arcpy.CreateObject("FieldMappings")
        fieldmapping.addTable(in_put)
        fieldmapping.addTable(output)
        fieldmapping = Mapa(fieldmapping, in_put, "N_SOL", "Número_de_Solicitud")
        fieldmapping = Mapa(fieldmapping, in_put, "FSOL", "Fecha_de_Solicitud")
        fieldmapping = Mapa(fieldmapping, in_put, "REC_SOL", "Recibido_por")
        fieldmapping = Mapa(fieldmapping, in_put, "PL_SOL", "Planchas")
        fieldmapping = Mapa(fieldmapping, in_put, "NTM_SOL", "Número_Total_Muestras")
        fieldmapping = Mapa(fieldmapping, in_put, "NCAJ_SOL", "Número_de_Caja")
        fieldmapping = Mapa(fieldmapping, in_put, "TMST_SOL", "Tipo_de_Muestra")
        fieldmapping = Mapa(fieldmapping, in_put, "CORP_SOL", "Coordinador_Proyecto")
        fieldmapping = Mapa(fieldmapping, in_put, "EMPO_SOL", "Empresa_Operadora")
        fieldmapping = Mapa(fieldmapping, in_put, "COR_SOL", "Corazonador")
        fieldmapping = Mapa(fieldmapping, in_put, "NPOZO_SOL", "Número_de_Pozo")
        fieldmapping = Mapa(fieldmapping, in_put, "PAEL_SOL", "Persona_Autoriza_Entrega")
        fieldmapping = Mapa(fieldmapping, in_put, "FAEL_SOL", "Fecha_Autorización_Entrega")
        fieldmapping = Mapa(fieldmapping, in_put, "ID_SOL", "Id_Solicitud")
        fieldmapping = Mapa(fieldmapping, in_put, "PROYECTO", "Nombre_del_Proyecto")
        fieldmapping = Mapa(fieldmapping, in_put, "COD_LIT", "Código_Litoteca")
        arcpy.AddMessage("...Cargando Solicitud ")
        arcpy.Append_management(in_put, output, "NO_TEST",fieldmapping)
except Exception as e:
    arcpy.AddMessage("Error Cargando Solicitud: " + e.message)

#### Cargue Muestra
try:
    in_put = geodatabase + os.sep + "Muestra_MAGNA"
    output = geodatabase + os.sep + "Muestra_Litoteca" + os.sep + "F33MLIT_MST_LIT"
    if arcpy.Exists(in_put):
        fieldmapping = arcpy.CreateObject("FieldMappings")
        fieldmapping.addTable(in_put)
        fieldmapping.addTable(output)
        fieldmapping = Mapa(fieldmapping, in_put, "TIP_COD_MST", "Tipo_Código")
        fieldmapping = Mapa(fieldmapping, in_put, "CORD_X_MST", "Coordenada_Este__m_")
        fieldmapping = Mapa(fieldmapping, in_put, "CORD_Y_MST", "Coordenada_Norte__m_")
        fieldmapping = Mapa(fieldmapping, in_put, "DAT", "Datum")
        fieldmapping = Mapa(fieldmapping, in_put, "ORGN", "Origen_de_Gauss")
        fieldmapping = Mapa(fieldmapping, in_put, "CPRL_MST", "Clasificación_Preliminar")
        fieldmapping = Mapa(fieldmapping, in_put, "TIPAN_MST", "Tipo_Análisis_Muestra")
        fieldmapping = Mapa(fieldmapping, in_put, "CTD", "Cantidad")
        fieldmapping = Mapa(fieldmapping, in_put, "UNDMED", "Unidad_de_Medida")
        fieldmapping = Mapa(fieldmapping, in_put, "CAJ", "Caja")
        fieldmapping = Mapa(fieldmapping, in_put, "OBS", "Observaciones")
        fieldmapping = Mapa(fieldmapping, in_put, "CLT_MST", "Colector_Muestra")
        fieldmapping = Mapa(fieldmapping, in_put, "FEC_MST", "Fecha_Muestra")
        fieldmapping = Mapa(fieldmapping, in_put, "UBI_FIS_MST", "Ubicación_Física")
        fieldmapping = Mapa(fieldmapping, in_put, "LAT_MST", "Latitud")
        fieldmapping = Mapa(fieldmapping, in_put, "LONG_MST", "Longitud")
        fieldmapping = Mapa(fieldmapping, in_put, "LOC_GEO_MST", "Localización_Geográfica")
        fieldmapping = Mapa(fieldmapping, in_put, "NMGC_MST", "Número_de_Campo")
        fieldmapping = Mapa(fieldmapping, in_put, "COD", "Código")
        fieldmapping = Mapa(fieldmapping, in_put, "NSOL", "Número_de_Solicitud")
except Exception as e:
    arcpy.AddMessage("Error Calculando Tipo Muestra solicitud: " + e.message)
#### Cargue Nucleo
try:
    arcpy.Append_management(in_put, output, "NO_TEST", fieldmapping)
except Exception as e:
    arcpy.AddMessage("Error Cargando solicitud: " + e.message)


try:
    in_put = geodatabase + os.sep + "Nucleo_MAGNA"
    output = geodatabase + os.sep + "Muestra_Litoteca" + os.sep + "F33NCL_NUCLEO"
    if arcpy.Exists(in_put):
        fieldmapping = arcpy.CreateObject("FieldMappings")
        fieldmapping.addTable(in_put)
        fieldmapping.addTable(output)
        fieldmapping = Mapa(fieldmapping, in_put, "CORD_X_NCL", "Coordenada_Este__m_")
        fieldmapping = Mapa(fieldmapping, in_put, "CORD_Y_NCL", "Coordenada_Norte__m_")
        fieldmapping = Mapa(fieldmapping, in_put, "LAT_NCL", "Latitud")
        fieldmapping = Mapa(fieldmapping, in_put, "LONG_NCL", "Longitud")
        fieldmapping = Mapa(fieldmapping, in_put, "NPOZO", "Número_Pozo")
        fieldmapping = Mapa(fieldmapping, in_put, "INT_NCL", "Intervalo")
        fieldmapping = Mapa(fieldmapping, in_put, "TOP_NCL", "Tope")
        fieldmapping = Mapa(fieldmapping, in_put, "DIAM", "Diametro")
        fieldmapping = Mapa(fieldmapping, in_put, "PREC", "Porcentaje_Recuperación")
        fieldmapping = Mapa(fieldmapping, in_put, "TIPAN_NCL", "TIipo_Análisis")
        fieldmapping = Mapa(fieldmapping, in_put, "NMGN", "Nombre_Núcleo")
        fieldmapping = Mapa(fieldmapping, in_put, "CAJ", "Caja")
        fieldmapping = Mapa(fieldmapping, in_put, "FRMN", "Formación")
        fieldmapping = Mapa(fieldmapping, in_put, "LOC_GEO_NCL", "Localización_Geográfica")
        fieldmapping = Mapa(fieldmapping, in_put, "ID_NCL", "Identificador_de_Núcleo")
        fieldmapping = Mapa(fieldmapping, in_put, "NSOL", "Número_de_Solicitud")
except Exception as e:
    arcpy.AddMessage("Error Cargando puntos: " + e.message)

try:
    arcpy.Append_management(in_put, output, "NO_TEST", fieldmapping)
except Exception as e:
    arcpy.AddMessage("Error Cargando información: " + e.message)
try:
    arcpy.CalculateField_management(geodatabase + os.sep + "Muestra_Litoteca" + os.sep + "F33MLIT_MST_LIT", "LAT_MST", expression1, "PYTHON", codeblock1)
    arcpy.CalculateField_management(geodatabase + os.sep + "Muestra_Litoteca" + os.sep + "F33NCL_NUCLEO", "LAT_NCL", expression1, "PYTHON", codeblock1)
except Exception as e:
    arcpy.AddMessage("Error Calculando Longitud: " + e.message)
try:
    arcpy.CalculateField_management(geodatabase + os.sep + "Muestra_Litoteca" + os.sep + "F33MLIT_MST_LIT", "LONG_MST", expression2, "PYTHON", codeblock2)
    arcpy.CalculateField_management(geodatabase + os.sep + "Muestra_Litoteca" + os.sep + "F33NCL_NUCLEO", "LONG_NCL", expression2, "PYTHON", codeblock2)
except Exception as e:
    arcpy.AddMessage("Error Calculando Latitud: " + e.message)

arcpy.AddMessage("...Borrando Temporales")
try:
    arcpy.Delete_management(geodatabase+os.sep+ "Solicitud")
    arcpy.Delete_management(geodatabase+os.sep+ "Muestra")
    arcpy.Delete_management(geodatabase+os.sep+ "Nucleo")
    arcpy.Delete_management(geodatabase+os.sep+"Muestra_MAGNA")
    arcpy.Delete_management(geodatabase+os.sep+"Nucleo_MAGNA")
    arcpy.Delete_management(geodatabase+os.sep+"Muestra_BOGOTA")
    arcpy.Delete_management(geodatabase+os.sep+"Nucleo_BOGOTA")
except Exception as e:
    arcpy.AddMessage("Error Borrando Temporales: "+ e.message)

if cargueSDE == "true":
    try:
        arcpy.AddMessage("...Cargando Informacion a SDE de Producción")
        arcpy.Append_management(geodatabase + os.sep + "Muestra_Litoteca" + os.sep + "F33MLIT_MST_LIT", geodatabaseSDE + os.sep + "MLIT.Muestra_Litoteca\MLIT.F33MLIT_MST_LIT", "NO_TEST")
        arcpy.Append_management(geodatabase + os.sep + "Muestra_Litoteca" + os.sep + "F33NCL_NUCLEO", geodatabaseSDE + os.sep + "MLIT.Muestra_Litoteca\MLIT.F33NCL_NUCLEO", "NO_TEST")
        arcpy.Append_management(geodatabase + os.sep + "F33SOL_SOLICITUD", geodatabaseSDE + os.sep + "MLIT.F33SOL_SOLICITUD", "NO_TEST")
    except Exception as e:
        arcpy.AddMessage("Error Cargando a SDE: "+ e.message)


