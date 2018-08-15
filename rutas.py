from os import walk

def ls(ruta = '.'):
    dir, subdirs, archivos = next(walk(ruta))
    print("Actual: ", dir)
    print("Subdirectorios: ", subdirs)
    print("Archivos: ", archivos)
    return archivos

ls(r"\\srv-ar1\sige$\GrupoSIG\Evidencias PV\Fernando\Evidencias\Evidencias_Informe_Semestral")
