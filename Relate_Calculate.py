import arcpy, os,sys



def ValoresEntrada(Feat,fields):
    datos = {}

    with arcpy.da.SearchCursor(Feat, fields) as cursor:
        for row in cursor:
           datos[row[0]] =row
    return datos

def actualizar(FeatOut,fields,fieldsOut,Featin,GeodatabaseSalida):
    valoresEntrada = ValoresEntrada(TablaRelacionada,fields)
    Numerador=0
    result = arcpy.GetCount_management(Featin)
    count = int(result.getOutput(0))
    Controlvalores = []
    edit = arcpy.da.Editor (GeodatabaseSalida)
    edit.startEditing ()
    edit.startOperation()
    with arcpy.da.UpdateCursor(FeatOut, fieldsOut) as cursor2:
        for row2 in cursor2:
            keyvalue=row2[0]
            if keyvalue in valoresEntrada:
                if keyvalue not in Controlvalores:
                    try:
                        Numerador = Numerador + 1
                        print "Actualizando Valor..."+ str(keyvalue)+ "....("+str(Numerador)+ " de "+str(count)+")"
                        row2[1]=1
                        cursor2.updateRow(row2)
                        Controlvalores.append(keyvalue)
                    except Exception as e:
                        print "Error..."+ e.message
    edit.stopOperation()
    edit.stopEditing("True")

print "Iniciando Proceso"


Tablas=[]

Tablas.append([r"C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.T_view_contratos",r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.EPIS\EPIS.CONTRATOS_EPIS_SGC','CONTRATO','CONTRATO_N','RELACIONADO'])
Tablas.append([r"C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.T_view_pozos",r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.EPIS\EPIS.POZOS_EPIS_SGC','UWI','UWI','RELACIONADO'])
Tablas.append([r"C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.T_view_sismica2d",r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.EPIS\EPIS.SISMICA2D_EPIS_SGC','PROGRAMA','SURVEY_NAM','RELACIONADO'])
Tablas.append([r"C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.T_view_sismica3d",r'C:\Users\fgonzalezf\Desktop\Conexiones\EPISODAPROD.sde\EPIS.EPIS\EPIS.SISMICA3D_EPIS_SGC','CONTRATO','CONTRATO','RELACIONADO'])



for table in Tablas:
    TablaRelacionada = table[0]
    FeatuareClassSalida=table[1]
    CampoIdentificadorin=table[2]
    CampoIdentificadorOut=table[3]
    CampoCalculo=table[4]
    GeodatabaseSalida= os.path.dirname(TablaRelacionada)
    actualizar(FeatuareClassSalida,[CampoIdentificadorin],[CampoIdentificadorOut,CampoCalculo],TablaRelacionada,GeodatabaseSalida)
