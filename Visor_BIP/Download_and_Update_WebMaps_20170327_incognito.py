#-------------------------------------------------------------------------------
# Name:        Download_and_Update_WebMaps
# Purpose:     DownloadWebMaps and save to mxd and json, replace in json and
#              upload again
# Author:      niue
#
# Created:     27/03/2017
# Copyright:   (c) niue 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Does not update the map online yet!
import arcrest, urllib, urllib2, json, arcpy

def readAndSave():
    # Read maps from Content and saves to mxd and json
        print(item.title+"...")
        webmap="http://sgcolombiano.maps.arcgis.com/sharing/rest/content/items/"+item.id+"/data?f=pjson"
        WebMap_as_JSON = urllib.urlopen(webmap).read()

        result = arcpy.mapping.ConvertWebMapToMapDocument(WebMap_as_JSON)

        mxd = result.mapDocument
        mxd.saveACopy(r"C:\temp\\"+item.title+".mxd")

        print("Map document saved")

        output_file=open(r"C:\temp\\"+item.title+".json", "w")
        output_file.write(WebMap_as_JSON)
        output_file.close()
        print("json saved")
        return(item.id, item.title)

def UpdateItem(username, itemID, itemTitle):
        '''Updates the input webmap with the new JSON loaded,
        uses urllib as a get request'''
        print(itemTitle+" upload...")
        url = 'http://sgcolombiano.maps.arcgis.com/sharing/rest/content/items/{}/update?f=pjson'.format(username, item.id)

        filein="C:/temp/"+item.title+".json"
        fileout="C:/temp/"+item.title+"_.json"

        f = open(filein,'r')
        filedata = f.read()
        f.close()

        newdata = filedata
        f = open(fileout,'w')
        f.write(newdata)
        f.close()

        JSON = open(fileout, 'r')
        jsondata = JSON.read()
        JSON.close()

        dumped = json.dumps(jsondata)
        data = {'async': 'True',
                'text': dumped}

        data = urllib.urlencode(data)
        request = urllib2.Request(url, data)
        response = urllib2.urlopen(request)

        print(item.title+" replaced")

        return json.loads(response.read())

if __name__ == '__main__':
    username = "fgonzalezf_SGColombiano"
    password = "Maidenfgf1"
    sh = arcrest.AGOLTokenSecurityHandler(username=username, password=password)
    admin = arcrest.manageorg.Administration(securityHandler=sh)
    content = admin.content
    # Get the logged in user
    currentUser = content.users.user()

    for item in currentUser.items:
        if item.type=="Web Map" and item.title=="Visor_EPIS":
            #readAndSave()
            UpdateItem(username, item.id, item.title)
