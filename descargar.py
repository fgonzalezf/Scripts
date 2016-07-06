from urllib import urlretrieve, urlcleanup
def status(count, data_size, total_data):
    """Llamado por cada bloque de datos recibido"""
    print count, data_size, total_data

def main():
    url = ("http://mirrors.ibiblio.org/eclipse/technology/epp/downloads/release/mars/2/eclipse-java-mars-2-win32-x86_64.zip")
    # Nombre del archivo a partir del URL
    filename = url[url.rfind("/") + 1:]
    while not filename:
        filename = raw_input("No se ha podido obtener el nombre del "
                             "archivo.\nEspecifique uno: ")

    print "Descargando %s..." % filename

    urlretrieve(url, filename, status)  # Descargar archivo
    urlcleanup()  #  Limpiar cache

    print "%s descargado correctamente." % filename
if __name__ == "__main__":
    main()

