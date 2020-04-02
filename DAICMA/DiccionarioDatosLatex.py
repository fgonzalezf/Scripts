import arcpy, os,sys
from pylatex import Document, Section, Subsection, Tabular, MultiColumn,\
    MultiRow
reload(sys)
sys.setdefaultencoding("Latin-1")

geodatabase=r"C:\Users\pache\Documents\nuevo\Integrada\DESCONTAMINA_2019.gdb"
#salida = r"C:\temp\Atlas\AGCQ_Atlas_Produccion.xlsx"
arcpy.env.workspace = geodatabase
doc = Document("Diccionario Datos")

listadatasets= arcpy.ListDatasets("*")

for Dataset in listadatasets:
    print Dataset
    section = Section(Dataset)
    datasetin= geodatabase+os.sep+Dataset
    arcpy.env.workspace= datasetin
    listfeat= arcpy.ListFeatureClasses("*")
    for fc in listfeat:
        test1 = Subsection(fc)
        listaCampos=arcpy.ListFields(fc)
        table1 = Tabular('|c|c|c|c|c|')
        table1.add_hline()
        table1.add_row((MultiColumn(5, align='|c|', data=fc),))
        table1.add_hline()
        table1.add_row(["Nombre de Campo","Alias","Tipo","Longitud","Descripcion"])
        table1.add_hline()
        X=1
        for field in listaCampos:

            if field.editable == True and field.type!="Geometry":
                X = X + 1
                table1.add_row((field.name.encode('Latin-1').title(), field.aliasName.encode('Latin-1').title(), field.type, field.length, " "))
                table1.add_hline()
        test1.append(table1)
        section.append(test1)
        print (fc)
    doc.append(section)
doc.generate_pdf(clean_tex=False)

