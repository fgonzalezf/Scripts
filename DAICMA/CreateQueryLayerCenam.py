# -*- coding: utf-8 -*-
import arcpy, os,sys


arcpy.env.overwriteOutput=True

#creacion de querys

sr = arcpy.SpatialReference(4326)
arcpy.MakeQueryLayer_management("Database Connections/SQLServer.sde",
                                "Victimas_Por_Hora",
                                """
                                SELECT
                                      ACCIDENTES_1.OBJECTID,
                                      ACCIDENTES_1.SHAPE,
                                      DATEPART(HOUR, ACCIDENTES_1.HORA___HH_MM_) AS HORA,
                                      VICTIMAS
                                    FROM dbo.ACCIDENTES AS ACCIDENTES_1
                                    INNER JOIN (SELECT
                                      MIN(DIVISION) AS DIVISION,
                                      MIN(OBJECTID) AS OBJECTID,
                                      DATEPART(HOUR, MAX(HORA___HH_MM_)) AS HORA,
                                      COUNT(*)
                                      AS VICTIMAS
                                    FROM dbo.ACCIDENTES AS ACCIDENTES
                                    GROUP BY DATEPART(HOUR, HORA___HH_MM_)) AS g
                                      ON ACCIDENTES_1.OBJECTID = g.OBJECTID
                                """,
                                "OBJECTID",
                                "POINT",
                                "4326",
                                sr)
arcpy.MakeQueryLayer_management("Database Connections/SQLServer.sde",
                                "Victimas_Por_Anio",
                                """
                                SELECT
                                  ACCIDENTES_1.OBJECTID,
                                  ACCIDENTES_1.SHAPE,
                                  ACCIDENTES_1.CONDICIÓN,
                                  YEAR(ACCIDENTES_1.FECHA___DD_MM_AAAA_) AS AÑO,
                                  VICTIMAS
                                FROM dbo.ACCIDENTES AS ACCIDENTES_1
                                INNER JOIN (SELECT
                                  MIN(DIVISION) AS DIVISION,
                                  MIN(OBJECTID) AS OBJECTID,
                                  YEAR(MIN(FECHA___DD_MM_AAAA_)) AS AÑO,
                                  COUNT(*) AS VICTIMAS
                                FROM dbo.ACCIDENTES AS ACCIDENTES
                                GROUP BY YEAR(FECHA___DD_MM_AAAA_),
                                         CONDICIÓN) AS g
                                  ON ACCIDENTES_1.OBJECTID = g.OBJECTID
                                """,
                                "OBJECTID",
                                "POINT",
                                "4326",
                                sr)

arcpy.MakeQueryLayer_management("Database Connections/SQLServer.sde",
                                "Victimas_Por_Division",
                                """
                                SELECT
                                  ACCIDENTES_1.OBJECTID,
                                  ACCIDENTES_1.SHAPE,
                                  ACCIDENTES_1.DIVISION,
                                  VICTIMAS
                                FROM dbo.ACCIDENTES AS ACCIDENTES_1
                                INNER JOIN (SELECT
                                  MIN(DIVISION) AS DIVISION,
                                  MIN(OBJECTID) AS OBJECTID,
                                  YEAR(MIN(FECHA___DD_MM_AAAA_)) AS AÑO,
                                  COUNT(*) AS VICTIMAS
                                FROM dbo.ACCIDENTES AS ACCIDENTES
                                GROUP BY DIVISION) AS g
                                  ON ACCIDENTES_1.OBJECTID = g.OBJECTID
                                """,
                                "OBJECTID",
                                "POINT",
                                "4326",
                                sr)
