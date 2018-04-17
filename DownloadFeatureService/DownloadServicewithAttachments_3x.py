import arcpy, urllib.request, urllib.parse, json, os, math, sys, linecache

def downloadservice3x(hostedFeatureService, agsService, baseURL, whereClause, agsFeatures, agsTable, username, password, outputFC, getAttachments, cwd):
    # Variables
##    hostedFeatureService = arcpy.GetParameterAsText(0)
##    agsService = arcpy.GetParameterAsText(1)

    baseURL = baseURL + "/query"

##    agsFeatures = arcpy.GetParameterAsText(3)
##    agsTable = arcpy.GetParameterAsText(4)
##    username = arcpy.GetParameterAsText(5)
##    password = arcpy.GetParameterAsText(6)
##    outputFC = arcpy.GetParameterAsText(7)
##    getAttachments = arcpy.GetParameterAsText(8)
##    cwd = arcpy.GetParameterAsText(9)

    # Check if ArcGIS for Desktop Standard license is available
    if getAttachments == 'true':
        try:
            import arceditor
        except:
            msg = 'ArcGIS for Desktop Standarad license is required to extract attachments'
            arcpy.AddError(msg)
            sys.exit()

    # Function to handle errors
    def PrintException(error):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        arcpy.AddError(error + ':  FILE: {}, LINE: {} \n\t "{}": {}'.format(filename, lineno, line.strip(), exc_obj))
        sys.exit()

    # Function to add domains for hosted feature services
    def addDomainsHosted(fc):
        params = {'f': 'pjson', 'token': token}
        data = urllib.parse.urlencode(params)
        data = data.encode('ascii') # data should be bytes
        req = urllib.request.Request(baseURL[:-6], data)
        response = urllib.request.urlopen(req)

        # Decode bytes to String
        data = response.read().decode("utf-8")

        # Convert string to dictionary
        json_acceptable_string = data.replace("'", "\"")
        data = json.loads(json_acceptable_string)

        # Check if domains exist
        try:
            if len(data['types'][0]['domains']) > 0:
                try:
                    desc = arcpy.Describe(os.path.dirname(fc))
                    if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory' or desc.workspaceFactoryProgID == 'esriDataSourcesGDB.FileGDBWorkspaceFactory':
                        if len(data['types'][0]['domains']) > 0:
                            arcpy.AddMessage("\nRetrieving geodatabase domains")
                            for domainField in (data['types'][0]['domains']):
                                # Create table of domains
                                domainTable = arcpy.env.scratchGDB + "\\domains"
                                arcpy.CreateTable_management(arcpy.env.scratchGDB, out_name="domains")
                                arcpy.AddField_management(domainTable, "Name", "TEXT", "", "", "500")
                                arcpy.AddField_management(domainTable, "Code", "TEXT", "", "", "500")
                                arcpy.AddField_management(domainTable, "Description", "TEXT", "", "", "500")

                                # Create Insert Cursor
                                fields = ['Name', 'Code', 'Description']
                                cursor = arcpy.da.InsertCursor(domainTable, fields)

                                # Insert domain information into table
                                for field in data['fields']:
                                    if field['name'] == domainField:
                                        domainType = str(field['domain']['type'])
                                        if domainType == 'codedValue':
                                            domainName = str(field['domain']['name'])
                                            codedValues = field['domain']['codedValues']
                                            for values in codedValues:
                                                ##arcpy.AddMessage("\t" + values['code'] + ":  " + values['name'])
                                                cursor.insertRow((domainName, values['code'], values['name']))
                                del cursor

                                # Get domain description
                                domainDescription = str(data['types'][0]['templates'][0]['description'])

                                # Add domain to geodatabase
                                try:
                                    arcpy.AddMessage("\tAdding domain " + domainName + " to geodatabase")
                                    arcpy.TableToDomain_management(domainTable, 'Code', 'Description', os.path.dirname(fc), domainName, domainDescription)
                                except Exception as e:
                                    if "CodedValueDomain already exists" in str(e):
                                        arcpy.AddWarning("\t\tThe value being added to the Coded Value Domain already exists")
                                    else:
                                        arcpy.AddWarning("\t\tError adding table to domain:  " + str(e))
                                try:
                                    arcpy.AddMessage("\tApplying domain " + domainName + " to field " + domainField)
                                    arcpy.AssignDomainToField_management(fc, domainField, domainName)
                                except Exception as e:
                                    arcpy.AddWarning("\t\tError adding domain to feature class:  " + str(e))
                except Exception as e:
                    arcpy.AddMessage("Error Creating Domains:  " + str(e))
                    pass

        except:
            pass

    # Function to add domains for AGS services
    def addDomainsAGS(fc):
        params = {'f': 'pjson', 'token': token}
        data = urllib.parse.urlencode(params)
        data = data.encode('ascii') # data should be bytes
        req = urllib.request.Request(baseURL[:-6], data)
        response = urllib.request.urlopen(req)

        # Decode bytes to String
        data = response.read().decode("utf-8")

        # Convert string to dictionary
        json_acceptable_string = data.replace("'", "\"")
        data = json.loads(json_acceptable_string)

        # Check for domains
        for field in data['fields']:
            if field['domain'] != None and field['domain']['type'] == 'codedValue':
                try:
                    desc = arcpy.Describe(os.path.dirname(fc))
                    if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory' or desc.workspaceFactoryProgID == 'esriDataSourcesGDB.FileGDBWorkspaceFactory':
                        arcpy.AddMessage("\nRetrieving geodatabase domains")
                        # Create table of domains
                        domainTable = arcpy.env.scratchGDB + "\\domains"
                        arcpy.CreateTable_management(arcpy.env.scratchGDB, out_name="domains")
                        arcpy.AddField_management(domainTable, "Name", "TEXT", "", "", "500")
                        arcpy.AddField_management(domainTable, "Code", "TEXT", "", "", "500")
                        arcpy.AddField_management(domainTable, "Description", "TEXT", "", "", "500")

                        fields = ['Name', 'Code', 'Description']
                        cursor = arcpy.da.InsertCursor(domainTable, fields)

                        domainField = (field['name'])
                        domainName = field['domain']['name']

                        for vals in field['domain']['codedValues']:
                            code = vals['code']
                            value = vals['name']
                            cursor.insertRow((domainName, code, value))

                        del cursor

                        # Add domain to geodatabase
                        try:
                            arcpy.AddMessage("\tAdding domain " + domainName + " to geodatabase")
                            arcpy.TableToDomain_management(domainTable, 'Code', 'Description', os.path.dirname(fc), domainName, "")
                        except Exception as e:
                            if "CodedValueDomain already exists" in str(e):
                                arcpy.AddWarning("The value being added to the CodedValueDomain already exists")
                            else:
                                arcpy.AddWarning("Error adding table to domain:  " + str(e))
                        try:
                            arcpy.AddMessage("\tApplying domain " + domainName + " to field " + domainField)
                            arcpy.AssignDomainToField_management(fc, domainField, domainName)
                        except Exception as e:
                            arcpy.AddMessage("Error adding domain to feature class:  " + str(e))

                except Exception as e:
                    arcpy.AddMessage("Error Creating Domains:  " + str(e))
                    pass

    from arcpy import env
    env.overwriteOutput = 1
    env.workspace = env.scratchGDB

    # Generate token for hosted feature service
    if hostedFeatureService == 'true':
        try:
            arcpy.AddMessage('\nGenerating Token\n')
            tokenURL = 'https://www.arcgis.com/sharing/rest/generateToken'
            params = {'f': 'pjson', 'username': username, 'password': password, 'referer': 'http://www.arcgis.com'}
            data = urllib.parse.urlencode(params)
            data = data.encode('ascii') # data should be bytes
            req = urllib.request.Request(tokenURL, data)
            response = urllib.request.urlopen(req)

            # Decode bytes to String
            data = response.read().decode("utf-8")

            # Convert string to dictionary
            json_acceptable_string = data.replace("'", "\"")
            d = json.loads(json_acceptable_string)

            token = d['token']
        except:
            token = ''

    # Genereate token for AGS feature service
    if agsService == 'true':
        try:
            arcpy.AddMessage('\nGenerating Token\n')
            server = baseURL.split("//")[1].split("/")[0]
            tokenURL = 'http://' + server + '/arcgis/admin/generateToken'
            params = {'username': username, 'password': password, 'client': 'requestip', 'f': 'pjson'}
            data = urllib.parse.urlencode(params)
            data = data.encode('ascii') # data should be bytes
            req = urllib.request.Request(tokenURL, data)
            response = urllib.request.urlopen(req)

            # Decode bytes to String
            data = response.read().decode("utf-8")

            # Convert string to dictionary
            json_acceptable_string = data.replace("'", "\"")
            d = json.loads(json_acceptable_string)

            token = d['token']
        except:
            token = ''
            pass

    # Return largest ObjectID
    if whereClause == '':
        whereClause = '1=1'
    params = {'where': whereClause, 'returnIdsOnly': 'true', 'token': token, 'f': 'json'}
    data = urllib.parse.urlencode(params)
    data = data.encode('ascii') # data should be bytes
    req = urllib.request.Request(baseURL, data)
    response = urllib.request.urlopen(req)
    data = response.read().decode("utf-8")
    json_acceptable_string = data.replace("'", "\"")
    data = json.loads(json_acceptable_string)

    try:
        data['objectIds'].sort()
    except:
        arcpy.AddError("\nURL is incorrect.  Or, Service is secure, please enter username and password.\n")
        sys.exit()

    OIDs = data['objectIds']
    count = len(data['objectIds'])
    iteration = int(data['objectIds'][-1])
    minOID = int(data['objectIds'][0]) - 1
    OID = data['objectIdFieldName']

    # Check to see if downloading a feature or tabular data
    if agsFeatures != 'true' and agsTable != 'true':
        arcpy.AddError("\nPlease check 'Downloading Feature Data' or 'Downloading Tabular Data'\n")
        sys.exit()

    # Code for downloading feature data
    if agsFeatures == 'true':
        if count < 1000:
            x = iteration
            y = minOID

            if whereClause != '1=1':
                ids = ','.join(str(x) for x in data['objectIds'])
                where = "{0} IN ({1})".format(OID, ids)
            else:
                where = OID + '>' + str(y) + 'AND ' + OID + '<=' + str(x)

            fields ='*'

            query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)
            fsURL = baseURL + query
            fs = arcpy.FeatureSet()

            try:
                fs.load(fsURL)
            except Exception as e:
                arcpy.AddError("Error loading features: " + str(e))
                sys.exit()

            if whereClause != '1=1':
                arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x) + ' in where clause')
            else:
                arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
            desc = arcpy.Describe(os.path.dirname(outputFC))
            if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
                outputFC2 = outputFC.split(".")[-1]
                try:
                    arcpy.FeatureClassToFeatureClass_conversion(fs, os.path.dirname(outputFC), outputFC2)
                except:
                    PrintException("Error Copying Features")
            else:
                try:
                    arcpy.FeatureClassToFeatureClass_conversion(fs, os.path.dirname(outputFC), os.path.basename(outputFC))
                except:
                    PrintException("Error Copying Features")



        else:
            if whereClause != '1=1':
                y = 0
                x = y + 185
                firstTime = 'True'

                ids = data['objectIds']
                newIteration = len(data['objectIds'])
            else:
                y = minOID
                x = minOID + 1000
                firstTime = 'True'

                ids = data['objectIds']
                newIteration = (math.ceil(iteration/1000.0) * 1000)

            while y <= newIteration:
                if x > int(newIteration):
                    x = newIteration

                if whereClause != '1=1':
                    whereIds = ()

                    for i in range(y, x):
                            whereIds += (ids[i],)

                    whereIds = ','.join(str(z) for z in whereIds)
                    where = "{0} IN ({1})".format(OID, whereIds)
                else:
                    where = OID + '>' + str(y) + 'AND ' + OID + '<=' + str(x)
                fields ='*'

                query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)
                fsURL = baseURL + query

                fs = arcpy.FeatureSet()

                try:
                    fs.load(fsURL)

                    if firstTime == 'True':
                        if whereClause != '1=1':
                            arcpy.AddMessage('Copying features with ObjectIDs from ' + str(data['objectIds'][y]) + ' to ' + str(data['objectIds'][x]) + ' in where clause')
                        else:
                            arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
                        desc = arcpy.Describe(os.path.dirname(outputFC))
                        if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
                            outputFC2 = outputFC.split(".")[-1]
                            try:
                                arcpy.FeatureClassToFeatureClass_conversion(fs, os.path.dirname(outputFC), outputFC2)
                            except:
                                PrintException("Error Copying Features")
                        else:
                            try:
                                arcpy.FeatureClassToFeatureClass_conversion(fs, os.path.dirname(outputFC), os.path.basename(outputFC))
                            except:
                                PrintException("Error Copying Features")
                                sys.exit()
                        firstTime = 'False'
                    else:
                        desc = arcpy.Describe(os.path.dirname(outputFC))
                        if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
                            if whereClause != '1=1':
                                try:
                                    arcpy.AddMessage('Copying features with ObjectIDs from ' + str(data['objectIds'][y]) + ' to ' + str(data['objectIds'][x]) + ' in where clause')
                                except:
                                    x -= 1
                                    arcpy.AddMessage('Copying features with ObjectIDs from ' + str(data['objectIds'][y]) + ' to ' + str(data['objectIds'][x]) + ' in where clause')
                            else:
                                arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
                            insertRows = arcpy.da.InsertCursor(outputFC, ["*","SHAPE@"])
                            searchRows = arcpy.da.SearchCursor(fs, ["*","SHAPE@"])
                            for searchRow in searchRows:
                                fieldList = list(searchRow)
                                insertRows.insertRow(fieldList)
                        elif desc.workspaceFactoryProgID == '':
                            if whereClause != '1=1':
                                try:
                                    arcpy.AddMessage('Copying features with ObjectIDs from ' + str(data['objectIds'][y]) + ' to ' + str(data['objectIds'][x]) + ' in where clause')
                                except:
                                    x -= 1
                                    arcpy.AddMessage('Copying features with ObjectIDs from ' + str(data['objectIds'][y]) + ' to ' + str(data['objectIds'][x]) + ' in where clause')
                            else:
                                arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
                            try:
                                arcpy.Append_management(fs, outputFC, "NO_TEST")
                            except:
                                PrintException("Error Copying Features")
                        else:
                            if whereClause != '1=1':
                                try:
                                    arcpy.AddMessage('Copying features with ObjectIDs from ' + str(data['objectIds'][y]) + ' to ' + str(data['objectIds'][x]) + ' in where clause')
                                except:
                                    x -= 1
                                    arcpy.AddMessage('Copying features with ObjectIDs from ' + str(data['objectIds'][y]) + ' to ' + str(data['objectIds'][x]) + ' in where clause')
                            else:
                                arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
                            try:
                                arcpy.Append_management(fs, outputFC)
                            except:
                                PrintException("Error Copying Features")
                except:
                    PrintException("Error occurred")

                if whereClause != '1=1':
                    x += 185
                    y += 185
                else:
                    x += 1000
                    y += 1000

        try:
            del searchRow, searchRows, insertRows
        except:
            pass

    # Code for downloading tabular data
    if agsTable == 'true':
        if count < 1000:
            if whereClause != '1=1':
                ids = ','.join(str(x) for x in data['objectIds'])
                where = "{0} IN ({1})".format(OID, ids)
            else:
                x = iteration
                y = minOID
                where = OID + '>' + str(y) + 'AND ' + OID + '<=' + str(x)

            fields ='*'

            query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)
            fsURL = baseURL + query

            fs = arcpy.RecordSet()
            try:
                fs.load(fsURL)
            except:
                PrintException("Error Loading Features")

            if whereClause != '1=1':
                arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x) + ' in where clause')
            else:
                arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
            desc = arcpy.Describe(os.path.dirname(outputFC))
            if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
                outputFC2 = outputFC.split(".")[-1]
                try:
                    arcpy.TableToTable_conversion(fs, os.path.dirname(outputFC), outputFC2)
                except:
                    PrintException("Error Copying Features")
            else:
                try:
                    arcpy.TableToTable_conversion(fs, os.path.dirname(outputFC), os.path.basename(outputFC))
                except:
                    PrintException("Error Copying Features")

        else:
            if whereClause != '1=1':
                y = 0
                x = y + 185
                firstTime = 'True'

                ids = data['objectIds']
                newIteration = len(data['objectIds'])
            else:
                y = minOID
                x = minOID + 1000
                firstTime = 'True'

                ids = data['objectIds']
                newIteration = (math.ceil(iteration/1000.0) * 1000)

            while y <= newIteration:
                if whereClause != '1=1':
                    whereIds = ()

                    if x > newIteration:
                        x = newIteration

                    for i in range(y, x):
                        whereIds += (ids[i],)

                    whereIds = ','.join(str(z) for z in whereIds)
                    where = "{0} IN ({1})".format(OID, whereIds)
                else:
                    where = OID + '>' + str(y) + 'AND ' + OID + '<=' + str(x)

                fields ='*'

                query = "?where={}&outFields={}&f=json&token={}".format(where, fields, token)
                fsURL = baseURL + query

                fs = arcpy.RecordSet()

                try:
                    fs.load(fsURL)

                    if firstTime == 'True':
                        if whereClause != '1=1':
                            arcpy.AddMessage('Copying features with ObjectIDs from ' + str(data['objectIds'][y]) + ' to ' + str(data['objectIds'][x]) + ' in where clause')
                        else:
                            arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
                        desc = arcpy.Describe(os.path.dirname(outputFC))
                        if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
                            outputFC2 = outputFC.split(".")[-1]
                            try:
                                arcpy.TableToTable_conversion(fs, os.path.dirname(outputFC), outputFC2)
                            except:
                                PrintException("Error Copying Features")
                        else:
                            try:
                                arcpy.TableToTable_conversion(fs, os.path.dirname(outputFC), os.path.basename(outputFC))
                            except:
                                PrintException("Error Copying Features")
                        firstTime = 'False'
                    else:
                        desc = arcpy.Describe(os.path.dirname(outputFC))
                        if whereClause != '1=1':
                            try:
                                arcpy.AddMessage('Copying features with ObjectIDs from ' + str(data['objectIds'][y]) + ' to ' + str(data['objectIds'][x]) + ' in where clause')
                            except:
                                x -= 1
                                arcpy.AddMessage('Copying features with ObjectIDs from ' + str(data['objectIds'][y]) + ' to ' + str(data['objectIds'][x]) + ' in where clause')
                        else:
                            arcpy.AddMessage('Copying features with ObjectIDs from ' + str(data['objects'][y]) + ' to ' + str(data['objects'][x]))
                        try:
                            arcpy.Append_management(fs, outputFC)
                        except:
                            PrintException("Error Copying Features")
                except:
                    PrintException("Error occurred")

                if whereClause != '1=1':
                    x += 185
                    y += 185
                else:
                    x += 1000
                    y += 1000

        try:
            del searchRow, searchRows, insertRows
        except:
            pass

    # Add Domains
    if hostedFeatureService == "true" and agsFeatures == "true":
        addDomainsHosted(outputFC)

    if hostedFeatureService == "true" and agsTable == "true":
        addDomainsAGS(outputFC)

    if agsService == "true":
        addDomainsAGS(outputFC)

    # Code for retrieving attachments
    if getAttachments == 'true':
        # Create Replica to retrieve attachments
        arcpy.AddMessage("\nRetrieving Attachments\n")
        crUrl = baseURL[0:-7] + 'createReplica'
        crValues = {'f' : 'json',
        'layers' : '0',
        'returnAttachments' : 'true',
        'supportsAttachmentsSyncDirection': 'bidirectional',
        'token' : token }

        data = urllib.parse.urlencode(crValues)
        data = data.encode('ascii') # data should be bytes
        req = urllib.request.Request(crUrl, data)
        response = urllib.request.urlopen(req)

        # Decode bytes to String
        data = response.read().decode("utf-8")

        # Convert string to dictionary
        json_acceptable_string = data.replace("'", "\"")
        crJson = json.loads(json_acceptable_string)

        try:
            crJson['URL'] = 'https:' + crJson['URL'].split(":")[-1]
            replicaUrl = crJson['URL'] + '?token=' + token
        except Exception as e:
            arcpy.AddWarning("\nService does not have 'Sync' operation enabled\n")
            sys.exit()
        urllib.request.urlretrieve(replicaUrl, cwd + os.sep + 'myLayer.json')

        f = open(cwd + os.sep + 'myLayer.json')
        lines = f.readlines()
        f.close()

        for line in lines:
            if not 'attachments' in line:
                arcpy.AddWarning("\nService does not contain attachments\n")
                sys.exit()
                os.remove(cwd + os.sep + 'myLayer.json')
                sys.exit()

        # Get Attachment
        with open(cwd + os.sep + 'myLayer.json') as data_file:
            data = json.load(data_file)

        if whereClause != '1=1':
            dict = {}
            x = 0
            while x <= len(data['layers'][0]['features']):
                try:
                    if data['layers'][0]['features'][x]['attributes'][OID] in OIDs:
                        try:
                            dict[data['layers'][0]['features'][x]['attributes'][OID]] = data['layers'][0]['features'][x]['attributes']['GlobalID']
                            x += 1
                        except KeyError:
                            dict[data['layers'][0]['features'][x]['attributes'][OID]] = data['layers'][0]['features'][x]['attributes']['globalid']
                            x += 1
                        except IndexError:
                            x += 1
                            pass
                    else:
                        x += 1
                except IndexError:
                    x += 1
                    pass

        else:
            dict = {}
            x = 0
            while x <= count:
                try:
                    dict[data['layers'][0]['features'][x]['attributes'][OID]] = data['layers'][0]['features'][x]['attributes']['GlobalID']
                    x += 1
                except KeyError:
                    dict[data['layers'][0]['features'][x]['attributes'][OID]] = data['layers'][0]['features'][x]['attributes']['globalid']
                    x += 1
                except IndexError:
                    x += 1
                    pass

        fc = outputFC
        try:
            arcpy.AddField_management(fc, "GlobalID_Str", "TEXT")
        except:
            PrintException("Error Adding Field")

        dictList = list(dict.keys())
        dictList.sort()

        x = 1
        y = 0
        while x <= count:
            with arcpy.da.UpdateCursor(fc, ["OID@", "GlobalID_Str"], "OBJECTID = " + str(x)) as cursor:
                for row in cursor:
                    row[1] = dict[dictList[y]]
                    cursor.updateRow(row)
            x += 1
            y += 1
        del cursor

        try:
            arcpy.EnableAttachments_management(fc)
        except:
            PrintException("Error Adding Attachments")
        try:
            arcpy.AddField_management(fc + "__ATTACH", "GlobalID_Str", "TEXT")
            arcpy.AddField_management(fc + "__ATTACH", "PhotoPath", "TEXT")
        except:
            PrintException("Error Adding Field")

        # Add Attachments
        # Create Match Table
        if whereClause != '1=1':
            attachmentGlobalIDs = []
            for x in data['layers'][0]['features']:
                if x['attributes'][OID] in OIDs:
                    attachmentGlobalIDs.append(x['attributes']['GlobalID'])

        try:
            for x in data['layers'][0]['attachments']:
                if whereClause != '1=1':
                    for attachmentGlobalID in attachmentGlobalIDs:
                        if x['parentGlobalId'] == attachmentGlobalID:
                            arcpy.AddMessage('match')
                            gaUrl = x['url']
                            gaFolder = cwd + os.sep + x['parentGlobalId']
                            if not os.path.exists(gaFolder):
                                os.makedirs(gaFolder)
                            gaName = x['name']
                            gaValues = {'token' : token }
                            gaData = urllib.parse.urlencode(gaValues)
                            try:
                                urllib.request.urlretrieve(url=gaUrl + '/' + gaName + '?' + gaData, filename=os.path.join(gaFolder, gaName))
                            except:
                                pass

                            rows = arcpy.da.InsertCursor(fc + "__ATTACH", ["GlobalID_Str", "PhotoPath"])
                            rows.insertRow((x['parentGlobalId'], cwd + os.sep + x['parentGlobalId'] + os.sep + x['name']))
                            del rows
                            hasrow = True

                else:
                    gaUrl = x['url']
                    gaFolder = cwd + os.sep + x['parentGlobalId']
                    if not os.path.exists(gaFolder):
                        os.makedirs(gaFolder)
                    gaName = x['name']
                    gaValues = {'token' : token }
                    gaData = urllib.parse.urlencode(gaValues)
                    try:
                        urllib.request.urlretrieve(url=gaUrl + '/' + gaName + '?' + gaData, filename=os.path.join(gaFolder, gaName))
                    except:
                        pass

            if whereClause == '1=1':
                rows = arcpy.da.InsertCursor(fc + "__ATTACH", ["GlobalID_Str", "PhotoPath"])
                for cmtX in data['layers'][0]['attachments']:
                    rows.insertRow((cmtX['parentGlobalId'], cwd + os.sep +cmtX['parentGlobalId'] + os.sep + cmtX['name']))
                    hasrow = True
                del rows

            if hasrow == True:
                try:
                    arcpy.AddAttachments_management(fc, 'GlobalID_Str', fc + '__ATTACH', 'GlobalID_Str', 'PhotoPath')
                except:
                    PrintException("Error Retrieving Attachments")

            try:
                arcpy.MakeTableView_management(fc + '__ATTACH', "tblView")
                arcpy.SelectLayerByAttribute_management("tblView", "NEW_SELECTION", "DATA_SIZE = 0")
                arcpy.DeleteRows_management("tblView")
                arcpy.DeleteField_management(fc + '__ATTACH', 'GlobalID_Str')
                arcpy.DeleteField_management(fc + '__ATTACH', 'PhotoPath')
            except Exception as e:
                arcpy.AddWarning("Error: " + str(e))
                pass
        except KeyError:
            pass

        os.remove(cwd + os.sep + 'myLayer.json')


