# -*- coding: latin1 -*-
import arcpy,os
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Modificar Textos MXD"
        self.alias = "Modificar Textos MXD"
        # List of tool classes associated with this toolbox
        self.tools = [Tool]

class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Modificar MXD"
        self.description = "Modificar Textos de Mxd Previamente Creado"
        self.canRunInBackground = False
        self.params = arcpy.GetParameterInfo()

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
        displayName="Seleccionar Mxd",
        name="Seleccionar_Mxd",
        datatype="DEMapDocument",
        parameterType="Required",
        direction="Input",
        multiValue=False)

        param1 = arcpy.Parameter(
        displayName='Valores Texto',
        name='Valores_Texto',
        datatype='GPValueTable',
        parameterType='Required',
        direction='Input')

        param2 = arcpy.Parameter(
        displayName='Geodatabase',
        name='Geodatabase',
        datatype='DEWorkspace',
        parameterType='Optional',
        direction='Input')

        param3 = arcpy.Parameter(
        displayName='Codigo de Barras',
        name='Codigo_Barras',
        datatype='DERasterDataset',
        parameterType='Optional',
        direction='Input')

        param4 = arcpy.Parameter(
        displayName='Carpeta de Resultados',
        name='Carpeta_Resultados',
        datatype='DEWorkspace',
        parameterType='Required',
        direction='Input')

        param1.columns = [['String', 'Nombre_Campo'], ['String', 'Valor']]
        param2.filter.list = ["Local Database"]
        param4.filter.list = ["File System"]
        #param1.values = [['NAME', 'SUM'],['Nombre', 'Suma']]
        params = [param4, param0, param1, param2, param3  ]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
            import string
            if parameters[1].altered and parameters[0].value and not parameters[2].altered:
                List=[]
                mxd = arcpy.mapping.MapDocument(parameters[1].valueAsText)
                for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                    X=elm.elementPositionX
                    Y=elm.elementPositionY
                    if not(X >=70 and X<=85 and Y>=11.5 and Y<=42):
                        if X >=74.4684 and X<=74.6684 and Y>=7.1773 and Y<=7.3773:
                                List.append(["IMAGENES SPOT",elm.text])
                                elm.name="IMAGENES SPOT"
                        if X >=81.8244 and X<=82.0244 and Y>=5.7286 and Y<=5.9286:
                                List.append(["IGAC",elm.text])
                                elm.name="IGAC"
                        if X >=74.4684 and X<=74.6684 and Y>=7.4722 and Y<=7.6722:
                                List.append(["AÑO IMAGENES",elm.text])
                                elm.name="IMAGENES RAPIDEYE"
                        if X >=74.4656 and X<=74.6656 and Y>=8.0519 and Y<=8.2519:
                                List.append(["CLASIFICACION CAMPO",elm.text])
                                elm.name="CLASIFICACION CAMPO"
                        if X >=74.4656 and X<=74.6656 and Y>=7.7884 and Y<=7.9884:
                                List.append(["ACTUALIZACION",elm.text])
                                elm.name="ACTUALIZACION"
                        if X >=74.4656 and X<=74.6656 and Y>=8.5435 and Y<=8.7435:
                                List.append(["COORDENADAS PLANAS",elm.text])
                                elm.name="COORDENADAS PLANAS"
                        if X >=74.4656 and X<=74.6656 and Y>=9.1076 and Y<=9.3076:
                                List.append(["COORDENADAS GEOGRAFICAS",elm.text])
                                elm.name="COORDENADAS GEOGRAFICAS"
                        if X >=74.4656 and X<=74.6656 and Y>=9.6007 and Y<=9.8007:
                                List.append(["ORIGEN DE LA ZONA",elm.text])
                                elm.name="ORIGEN DE LA ZONA"
                        if X >=74.4656 and X<=74.6656 and Y>=9.834 and Y<=10.034:
                                List.append(["PROYECCION CARTOGRAFICA",elm.text])
                                elm.name="PROYECCION CARTOGRAFICA"
                        if X >=74.4656 and X<=74.6656 and Y>=10.3007 and Y<=10.5007:
                                List.append(["ELIPSOIDE",elm.text])
                                elm.name="ELIPSOIDE"
                        if X >=74.4656 and X<=74.6656 and Y>=10.6007 and Y<=10.8007:
                                List.append(["DATUM GEODESICO",elm.text])
                                elm.name="DATUM GEODESICO"
                        if X >=74.4656 and X<=74.6656 and Y>=10.8639 and Y<=11.0639:
                                List.append(["PROYECTO",elm.text])
                                elm.name="PROYECTO"
                        if X >=76.5422 and X<=76.7422 and Y>=44.3037 and Y<=44.5037:
                                List.append(["AÑO PLANCHA",elm.text])
                                elm.name="AÑO PLANCHA"
                        if X >=79 and X<=81 and Y>=48.0888 and Y<=48.2888:
                                List.append(["PLANCHA SUPERIOR",elm.text])
                                elm.name="PLANCHA SUPERIOR"
                        if X >=1 and X<=3 and Y>=1.7746 and Y<=1.9746:
                                List.append(["PLANCHA INFERIOR",elm.text])
                                elm.name="PLANCHA INFERIOR"
                        if X >=1.8219 and X<=2.0219 and Y>=48.1517 and Y<=48.3517:
                                List.append(["DEPARTAMENTO",elm.text])
                                elm.name="DEPARTAMENTO"
                        if X >=62.4204 and X<=62.6204 and Y>=45.5006 and Y<=45.7006:
                                List.append(["NORTE SUPERIOR DERECHA",elm.text])
                                elm.name="NORTE SUPERIOR DERECHA"
                        if X >=4.4025 and X<=4.6025 and Y>=45.45 and Y<=45.65:
                                List.append(["NORTE SUPERIOR IZQUIERDA",elm.text])
                                elm.name="NORTE SUPERIOR IZQUIERDA"
                        if X >=3.9 and X<=4.1 and Y>=43.4852 and Y<=43.6852:
                                List.append(["ESTE SUPERIOR IZQUIERDA",elm.text])
                                elm.name="ESTE SUPERIOR IZQUIERDA"
                        if X >=64.5006 and X<=64.7006 and Y>=43.3826 and Y<=43.5826:
                                List.append(["ESTE SUPERIOR DERECHA",elm.text])
                                elm.name="ESTE SUPERIOR DERECHA"
                        if X >=62.3364 and X<=62.5364 and Y>=4.95 and Y<=5.15 :
                                List.append(["NORTE INFERIOR DERECHA",elm.text])
                                elm.name="NORTE INFERIOR DERECHA"
                        if X >=4.405 and X<=4.605 and Y>=4.95 and Y<=5.15:
                                List.append(["NORTE INFERIOR IZQUIERDA",elm.text])
                                elm.name="NORTE INFERIOR IZQUIERDA"
                        if X >=64.4428 and X<=64.6428 and Y>=5.3715 and Y<=5.5715:
                                List.append(["ESTE INFERIOR DERECHA",elm.text])
                                elm.name="ESTE INFERIOR DERECHA"
                        if X >=3.9509 and X<=4.1509 and Y>=5.3953 and Y<=5.5953:
                                List.append(["ESTE INFERIOR IZQUIERDA",elm.text])
                                elm.name="ESTE INFERIOR IZQUIERDA"
                        if X>=70.3184 and X<=70.7184 and Y>=7.472200000000001 and Y<=7.6722:
                                List.append(["ENCABEZADO IMAGENES SATELITALES",elm.text])
                                elm.name="ENCABEZADO IMAGENES SATELITALES"
                        if X>=70.3184 and X<=70.7184 and Y>=10.600700000000002 and Y<=10.8007:
                                List.append(["ENCABEZADO DATUM GEODESICO",elm.text])
                                elm.name="ENCABEZADO DATUM GEODESICO"
                        if X>=70.3184 and X<=70.7184 and Y>=8.8002 and Y<=9.0002:
                                List.append(["ENCABEZADO COORDENADAS PLANAS",elm.text])
                                elm.name="ENCABEZADO COORDENADAS PLANAS"
                        if X>=70.3184 and X<=70.7184 and Y>=7.788400000000001 and Y<=7.9884:
                                List.append(["ENCABEZADO ACTUALIZACION",elm.text])
                                elm.name="ENCABEZADO ACTUALIZACION"
                        if X>=70.3184 and X<=70.7184 and Y>=9.600700000000002 and Y<=9.8007:
                                List.append(["ENCABEZADO ORIGEN DE LA ZONA",elm.text])
                                elm.name="ENCABEZADO ORIGEN DE LA ZONA"
                        if X>=70.3184 and X<=70.7184 and Y>=8.051900000000002 and Y<=8.251900000000001:
                                List.append(["ENCABEZADO CLASIFICACION",elm.text])
                                elm.name="ENCABEZADO CLASIFICACION"
                        if X>=70.3184 and X<=70.7184 and Y>=9.3643 and Y<=9.5643:
                                List.append(["ENCABEZADO COORDENADAS GEOGRAFICAS",elm.text])
                                elm.name="ENCABEZADO COORDENADAS GEOGRAFICAS"
                        if X>=70.3184 and X<=70.7184 and Y>=10.064300000000001 and Y<=10.2643:
                                List.append(["ENCABEZADO PROYECCION CARTOGRAFICA",elm.text])
                                elm.name="ENCABEZADO PROYECCION CARTOGRAFICA"
                        if X>=70.3184 and X<=70.7184 and Y>=10.3007 and Y<=10.5007:
                                List.append(["ENCABEZADO ELIPSOIDE",elm.text])
                                elm.name="ENCABEZADO ELIPSOIDE"
                        if X>=70.3184 and X<=70.7184 and Y>=10.863900000000001 and Y<=11.0639:
                                List.append(["ENCABEZADO PROYECTO",elm.text])
                                elm.name="ENCABEZADO PROYECTO"
                        if X>=25 and X<=55 and Y>=48 and Y<=49:
                                List.append(["MUNICIPIO",elm.text])
                                elm.name="MUNICIPIO"

                mxd.saveACopy(parameters[0].valueAsText + os .sep +os.path.basename(parameters[1].valueAsText))
                del mxd
                parameters[2].value=List
            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #parameters[1].value = [['NAME', 'SUM'],['Nombre', 'Suma']]
            return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    def initializeParameters(self):
      # Set the input file type to our recognized options file suffixes
      #
      return

    def execute(self, parameters, messages):
            """The source code of the tool."""
            mxd = arcpy.mapping.MapDocument(parameters[0].valueAsText + os .sep +os.path.basename(parameters[1].valueAsText))
            for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                for par in parameters[2].value:
                    if elm.name==str(par[0].encode("utf8")):
                        elm.text=str(par[1].encode("utf8"))

            ListaDataframe=arcpy.mapping.ListDataFrames(mxd)
            NombresDataframe={}
            i=0
            for dataframe in ListaDataframe:
                NombresDataframe[dataframe.name] = i
                arcpy.AddMessage(dataframe.name)
                i += 1
            pathWorkspace =""
            if parameters[3].value:
                if "Layers" in NombresDataframe.keys():
                    dataframeLayer=arcpy.mapping.ListDataFrames(mxd)[NombresDataframe["Layers"]]
                    for lyr in arcpy.mapping.ListLayers(mxd,"*",dataframeLayer):
                        if not lyr.isGroupLayer and lyr.isFeatureLayer:
                            pathWorkspace=lyr.workspacePath
                            break
                    mxd.findAndReplaceWorkspacePaths(pathWorkspace,parameters[3].valueAsText)
                    arcpy.AddMessage(parameters[3].valueAsText)
            if parameters[4].value:
                if "CODIGODEBARRAS" in NombresDataframe.keys():
                    arcpy.AddMessage(str(NombresDataframe["CODIGODEBARRAS"]))
                    dataframeLayer=arcpy.mapping.ListDataFrames(mxd)[NombresDataframe["CODIGODEBARRAS"]]
                    for lyr in arcpy.mapping.ListLayers(mxd,"*",dataframeLayer):
                        if not lyr.isGroupLayer and lyr.isRasterLayer:
                            pathWorkspace=lyr.workspacePath
                            lyr.replaceDataSource(os.path.dirname(parameters[4].valueAsText),"RASTER_WORKSPACE",os.path.basename(parameters[4].valueAsText))
                            break
                    arcpy.AddMessage(pathWorkspace)
            mxd.save()
            arcpy.mapping.ExportToPDF(mxd,parameters[0].valueAsText + os .sep +os.path.basename(parameters[1].valueAsText).replace(".mxd",".pdf"))
            del mxd
            return
