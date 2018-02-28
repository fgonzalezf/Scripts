#!/usr/bin/python
# -*- coding: utf-8 -*-
import arcpy, os, sys

Geodatabase=r"E:\Scripts\SDE.sde"
tablaDepartamentos=r"E:\Scripts\SDE.sde\SDE.dbo.depto_victimas"
tablaMunicipios=r"E:\Scripts\SDE.sde\SDE.dbo.muni_victimas"
featDepartamentos=r"E:\Scripts\SDE.sde\SDE.DBO.VICTIMAS\SDE.DBO.Departamento_Victimas"
featMunicipios =r"E:\Scripts\SDE.sde\SDE.DBO.VICTIMAS\SDE.DBO.Municipio_Victimas"

#Mapeo Campos

CamposDepartamentos = {"COD_DEPART":"COD_DANE",
                       "CIVIL":"CIVIL",
                       "FUERZA_PUBLICA":"FUERZA_PUBLICA",
                       "MASCULINO":"MASCULINO",
                       "FEMENINO":"FEMENINO",
                       "SIN_INFORMACION":"SIN_INFORMACION",
                       "HERIDO":"HERIDO",
                       "MUERTO":"MUERTO",
                       "MAYOR_DE_18_AÑOS":"MAYOR_18",
                       "MENOR_DE_18_AÑOS":"MENOR_18",
                       "TOTALES":"TOTALES"
                       }
CamposMunicipios = {"COD_MUNI":"COD_DANE",
                    "CIVIL":"CIVIL",
                    "FUERZA_PUBLICA":"FUERZA_PUBLICA",
                    "MASCULINO":"FEMENINO",
                    "FEMENINO":"MASCULINO",
                    "SIN_INFORMACION":"SIN_INFORMACION",
                    "HERIDO":"HERIDO",
                    "MUERTO":"MUERTO",
                    "MAYOR_DE_18_AÑOS":"MAYOR_18",
                    "MENOR_DE_18_AÑOS":"MENOR_18",
                    "TOTALES":"TOTALES"
                    }

CamposDepEntrada=sorted(CamposDepartamentos.keys())
CamposMunEntrada=sorted(CamposMunicipios.keys())

CamposDepSalida=sorted(CamposDepartamentos.values())
CamposMunSalida=sorted(CamposMunicipios.values())

print CamposDepEntrada
print CamposDepSalida

print CamposMunEntrada
print CamposMunSalida

edit = arcpy.da.Editor (Geodatabase)
edit.startEditing ()
edit.startOperation()

with arcpy.da.SearchCursor(tablaDepartamentos, CamposDepEntrada) as cursor:
    for row in cursor:
        expresion = "COD_DANE ="+str(int(row[1])).strip()

        with arcpy.da.UpdateCursor(featDepartamentos, CamposDepSalida, expresion) as cursor2:
            for row2 in cursor2:
                print row2[1]
                if int(row2[1])==int(row[1]):
                    print expresion
                    row2[0]=row[0]
                    row2[2]=row[2]
                    row2[3]=row[3]
                    row2[4]=row[4]
                    row2[5]=row[5]
                    row2[6]=row[6]
                    row2[7]=row[7]
                    row2[8]=row[8]
                    row2[9]=row[9]
                    row2[10]=row[10]
                    cursor2.updateRow(row2)

with arcpy.da.SearchCursor(tablaMunicipios, CamposMunEntrada) as cursor:
    for row in cursor:
        expresion = "COD_DANE ="+str(int(row[1])).strip()

        with arcpy.da.UpdateCursor(featMunicipios, CamposMunSalida, expresion) as cursor2:
            for row2 in cursor2:
                print row2[1]
                if int(row2[1])==int(row[1]):
                    print expresion
                    row2[0]=row[0]
                    row2[2]=row[2]
                    row2[3]=row[3]
                    row2[4]=row[4]
                    row2[5]=row[5]
                    row2[6]=row[6]
                    row2[7]=row[7]
                    row2[8]=row[8]
                    row2[9]=row[9]
                    row2[10]=row[10]
                    cursor2.updateRow(row2)

edit.stopOperation()
edit.stopEditing("True")





