__author__ = 'fgonzalezf'
import arcpy,os,sys

host=r"http://srvags.sgc.gov.co/Archivos_Geoportal"
carpeta=r"D:\Pruebas\Estandares"

arcpy.env.workspace= carpeta

#Lista de carpetas
Lista1= arcpy.ListWorkspaces("*","Folder")

for folder1 in Lista1:
    arcpy.env.workspace=folder1
    Lista2=arcpy.ListWorkspaces("*","Folder")
    for folder2 in Lista2:
        arcpy.env.workspace=folder2
        ListaArch= arcpy.ListFiles()
        for file in ListaArch:
            print host +r"/" +os.path.basename(carpeta)+ r"/" +os.path.basename(folder1)+ r"/"+os.path.basename(folder2)+r"/"+os.path.basename(file)






