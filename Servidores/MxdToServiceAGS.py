# Publishes a service to machine myserver using USA.mxd
# A connection to ArcGIS Server must be established in the
#  Catalog window of ArcMap before running this script
import arcpy,os
# Define local variables
wrkspc = r'C:\Users\fgonzalezf\Downloads\pruebas\MXD'
con = r'C:\Users\fgonzalezf\Downloads\pruebas\arcpruonsrvagspru.sgc.gov.co(admin).ags'


Servicios=[['C://Users//fgonzalezf//Downloads//pruebas//MXD//Amenaza_Sismica//Periodo_Retorno_75.MapServer//Periodo_Retorno_75.mxd','Periodo_Retorno_75','Amenaza_Sismica','Amenaza_Sismica','Sismica'],
           ['C://Users//fgonzalezf//Downloads//pruebas//MXD//Amenaza_Sismica//Periodo_Retorno_225.MapServer//Periodo_Retorno_225.mxd','Periodo_Retorno_225', 'Amenaza_Sismica','Amenaza_Sismica','Sismica'],
           ['C://Users//fgonzalezf//Downloads//pruebas//MXD//Amenaza_Sismica//Periodo_Retorno_475.MapServer//Periodo_Retorno_475.mxd','Periodo_Retorno_475','Amenaza_Sismica','Amenaza_Sismica','Sismica'],
           ['C://Users//fgonzalezf//Downloads//pruebas//MXD//Amenaza_Sismica//Periodo_Retorno_975.MapServer//Periodo_Retorno_975.mxd','Periodo_Retorno_975','Amenaza_Sismica','Amenaza_Sismica','Sismica'],
           ['C://Users//fgonzalezf//Downloads//pruebas//MXD//Amenaza_Sismica//Periodo_Retorno_2475.MapServer//Periodo_Retorno_2475.mxd','Periodo_Retorno_2475','Amenaza_Sismica','Amenaza_Sismica','Sismica']]
for serv in Servicios:
    mapDoc = serv[0]
    # Provide path to connection file
    # To create this file, right-click a folder in the Catalog window and
    #  click New > ArcGIS Server Connection

    # Provide other service details
    service = serv[1]
    folder_name = serv[2]
    print folder_name
    sddraft = wrkspc + service + '.sddraft'
    sd = wrkspc + service + '.sd'
    summary = serv[3]
    tags = serv[4]
    # Create service definition draft
    arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service, 'ARCGIS_SERVER', con, True, folder_name, summary, tags)
    # Analyze the service definition draft
    analysis = arcpy.mapping.AnalyzeForSD(sddraft)
    # Print errors, warnings, and messages returned from the analysis
    print "The following information was returned during analysis of the MXD:"
    for key in ('messages', 'warnings', 'errors'):
      print '----' + key.upper() + '---'
      vars = analysis[key]
      for ((message, code), layerlist) in vars.iteritems():
        print '    ', message, ' (CODE %i)' % code
        print '       applies to:',
        for layer in layerlist:
            print layer.name,
        print
    # Stage and upload the service if the sddraft analysis did not contain errors
    if analysis['errors'] == {}:
        # Execute StageService. This creates the service definition.
        arcpy.StageService_server(sddraft, sd)
        # Execute UploadServiceDefinition. This uploads the service definition and publishes the service.
        arcpy.UploadServiceDefinition_server(sd, con)
        print "Service successfully published"
    else:
        print "Service could not be published because errors were found during analysis."
    print arcpy.GetMessages()