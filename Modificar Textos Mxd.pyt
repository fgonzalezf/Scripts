import arcpy


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


        param1.columns = [['String', 'Nombre_Campo'], ['String', 'Valor']]

        params = [param0, param1]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        import string
        if self.params[0].value:

            """Modify the values and properties of parameters before internal
            validation is performed.  This method is called whenever a parameter
            has been changed."""
            #self.params[1].values = ['NAME', 'SUM']
            pass


        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    def initializeParameters(self):
      # Set the input file type to our recognized options file suffixes
      #
      self.params[1].filter.list = ["opt56", "opt57", "globalopt"]
      return


    def execute(self, parameters, messages):
        """The source code of the tool."""
        return
