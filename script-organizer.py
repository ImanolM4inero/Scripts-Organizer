import os
import shutil

print("**********************************************")
print("Bienvenido a tu script para organizar carpetas")
print("**********************************************")

# Ruta de la carpeta de descargas
ruta_descargas = r"C:\Downloads"

# Rutas de las subcarpetas
ruta_archivos = os.path.join(ruta_descargas, "Archivos")
ruta_documentos = os.path.join(ruta_descargas, "Documentos")
ruta_programas = os.path.join(ruta_descargas, "Programas")

# Crear las subcarpetas si no existen
for ruta in [ruta_archivos, ruta_documentos, ruta_programas]:
    if not os.path.exists(ruta):
        os.makedirs(ruta)

# Obtener la lista de archivos en la carpeta de descargas
archivos = os.listdir(ruta_descargas)

# Organizar los archivos en las subcarpetas correspondientes
for archivo in archivos:
    ruta_archivo = os.path.join(ruta_descargas, archivo)
    if os.path.isfile(ruta_archivo):
        extension = os.path.splitext(archivo)[1][1:].lower()  # Obtener la extensión del archivo
        if extension in ["txt", "pdf", "doc", "docx"]:
            shutil.move(ruta_archivo, os.path.join(ruta_documentos, archivo))
        elif extension in ["jpg", "png", "gif"]:
            shutil.move(ruta_archivo, os.path.join(ruta_archivos, archivo))
        elif extension in ["exe", "msi"]:
            shutil.move(ruta_archivo, os.path.join(ruta_programas, archivo))

print("<=================================================>")
print("<=================================================>")
print("Listo..... Tus archivos ya se encuentan organizados")
print("<=================================================>")
print("<=================================================>")
