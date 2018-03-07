#-------------------------------------------------------------------------------
# Name:        Download Service with Attachments
# Purpose:     Download ArcGIS Online Hosted Feature Services or ArcGIS Server
#              Map/Feature Services
#
# Author:      jskinner
#-------------------------------------------------------------------------------

import sys, os, arcpy

# Check if running tool from ArcGIS Pro or from ArcGIS Desktop
if 'arcgispro' in str(os.path.basename(sys.executable).lower()):
    import DownloadServicewithAttachments_3x
    DownloadServicewithAttachments_3x.downloadservice3x(arcpy.GetParameterAsText(0), arcpy.GetParameterAsText(1), arcpy.GetParameterAsText(2),
        arcpy.GetParameterAsText(3), arcpy.GetParameterAsText(4), arcpy.GetParameterAsText(5), arcpy.GetParameterAsText(6), arcpy.GetParameterAsText(7),
        arcpy.GetParameterAsText(8), arcpy.GetParameterAsText(9), arcpy.GetParameterAsText(10))

else:
    import DownloadServicewithAttachments_2x
    DownloadServicewithAttachments_2x.downloadservice2x(arcpy.GetParameterAsText(0), arcpy.GetParameterAsText(1), arcpy.GetParameterAsText(2),
        arcpy.GetParameterAsText(3), arcpy.GetParameterAsText(4), arcpy.GetParameterAsText(5), arcpy.GetParameterAsText(6), arcpy.GetParameterAsText(7),
        arcpy.GetParameterAsText(8), arcpy.GetParameterAsText(9), arcpy.GetParameterAsText(10))