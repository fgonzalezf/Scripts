
import locale, arcpy

locale.setlocale(locale.LC_ALL,"american")

arcpy.MapToKML_conversion(r"C:\Users\fgonzalezf\Downloads\Metalogenia\Mapa_metalogenico_2018_new.mxd","Layers",r"C:\Users\fgonzalezf\Downloads\Metalogenia\Metalogenico_Final_1.kmz",1,'NO_COMPOSITE','VECTOR_TO_VECTOR',"",1024,96,'CLAMPED_TO_GROUND')