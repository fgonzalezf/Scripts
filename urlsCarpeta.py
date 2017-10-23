__author__ = 'fgonzalezf'

import os,sys
from os import walk,getcwd
CarpetaBase=r"C:\Users\fgonzalezf\Documents\Estandares"
borrar=r"C:\Users\fgonzalezf\Documents"
urlBase="https://srvags.sgc.gov.co"

for root, dirs, files in os.walk(CarpetaBase, topdown=False):
    for name in files:
        print(os.path.join(root, name)).replace(borrar,urlBase).replace("\\","/")

