from PIL import Image
import os,sys
from os import walk,getcwd

CarpetaBase = r"C:\Users\fgonzalezf\Downloads\Atlas_geoquimico_2018"

for root, dirs, files in os.walk(CarpetaBase, topdown=False):

    for file in files:
        print (root+os.sep+file)
        image_file = Image.open(root+os.sep+file)
        image_file.save(root+os.sep+file[:-3]+".svg")