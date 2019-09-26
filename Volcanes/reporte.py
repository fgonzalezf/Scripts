import registrant
reporter = registrant.Reporter(
    r"C:\Users\APN\Downloads\Geomorfologia_Vacia_Fer\Geomorfologia_Vacia_Fer.mdb", r"C:\Temp"
)
reporter.gdb2html()
print(reporter.report_file_path)